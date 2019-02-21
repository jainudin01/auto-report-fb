#-*-coding:utf-8-*-
# Fb Mass Reports Account
# Created By Deray

import bs4
import json
import threading
import cookielib
import mechanize

class reports(threading.Thread):
	def __init__(self,email,pw,target):
		threading.Thread.__init__(self)
		self.email = email
		self.pw = pw
		self.tg = target
	def run(self):
		br = mechanize.Browser()
		url="https://mbasic.facebook.com"
		br.set_handle_equiv(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.set_cookiejar(cookielib.LWPCookieJar())
		br.addheaders = [
			(
			"User-Agent","Mozilla/5.0 (Linux; U; Android 5.1)"
			)
		]
		br.open("https://mbasic.facebook.com")
		br.select_form(nr=0)
		br.form["email"] = "{}".format(
			self.email
		)
		br.form["pass"]  = "{}".format(
			self.pw
		)
		br.submit()
		br.open(
		"https://mbasic.facebook.com/{}".format(
			self.tg
			)
		)
		bb = bs4.BeautifulSoup(
		br.response().read(),
			features = "html.parser"
		)
		for x in bb.find_all("a",href=True):
			if "rapid_report" in x["href"]:
				kntl=x["href"]
		br.open(kntl)
		br._factory.is_html=True
		j = json.dumps(
			{
			"fake":"profile_fake_account",
			"action_key":"FRX_PROFILE_REPORT_CONFIRMATION",
			"checked":"yes"
			}
		)
		js = json.loads(j)
		br.select_form(nr=0)
		br.form["tag"] =[js["fake"]]
		br.submit()
		br._factory.is_html=True
		br.select_form(nr=0)
		try:
			br.form["action_key"] = [js["action_key"]]
		except:
			return False
		br.submit()
		br._factory.is_html = True
		try:
			br.select_form(nr=0)
			br.form["checked"] = [js["checked"]]
			br.submit()
			res=br.response().read()
			if "Terima kasih atas masukan Anda." in res:
				print "[*] Reported."
			else:
				print "[-] Unreported."
		except:
			print "\r[-] Already Reports."