import sys
import urllib
import httplib
from subprocess import call
from selenium import webdriver
import convertHex
import grossTonnageParse
import psycopg2

#This function extracts the desired information by providing the original mainStr and the string before and after the desired information
def find(Str, front, back):
    startIdx = Str.find(front) + len(front)
    offset = Str[startIdx:].find(back)
    endIdx = startIdx + offset
    return Str[startIdx:endIdx]

#this function extracts the sessionID
def getSessID(s):
	startIdx = s.find("session=")+len("session=")
	s=s[startIdx:]
	endIdx = s.find("&")
	sessID = s[:endIdx]
	return sessID

#grosstonnage.com account, password and the mmsi number of the vessel to be crawled must be input as system argument in the command line
def main(account, password, mmsi):
	conn = httplib.HTTPConnection('www.grosstonnage.com')
	conn.request("GET","")
	r1=conn.getresponse()
	s=r1.read()
	sessID = getSessID(s)
	
	#use the session ID, account and password to get the arrive at the login page
	conn.request("GET","/LOGIN/logon.php?session="+sessID+"&syslng=ing&sysmen=-1&sysind=-1&syssub=-1&sysfnt=0&A4Iuser="+account+"&A4Ipassword="+password+"&from=OBJ&callingpage=[VESSEL]&vck=@C3@A4@94@9A@CE@16@E7@7E@E5@AC@0E@CCB@2C@0E@22&welcome=no")
	
	r2=conn.getresponse()
	loginPage=r2.read()
	sessID = getSessID(loginPage)
	#print sessID

	#construct the url of the vessel search page with the vessel mmsi input in the search form
	url = "http://www.grosstonnage.com/index.php?session="+sessID+"&syslng=ing&sysmen=-1&sysind=-1&syssub=-1&sysfnt=0&code=RESULT&str="+mmsi
	conn.request("GET",url)
	r3=conn.getresponse()
	infoPage=r3.read()

	f = urllib.urlopen(url)
	#open a webdriver object in Firefox and execute the vessel
	browser = webdriver.Firefox()
	browser.get(url)
	browser.execute_script("return gosearch()")

	htmlcode = browser.page_source.encode('utf-8')
	shipInfo = convertHex.main(htmlcode)
	#get the link to the detailed information page of the vessel
	link = browser.current_url+"&info=EI#EI"

	#parse the detailed vessel information page using the grossTonnageParse script to parse and store relevant ship information in the local database
	browser.get(link)
	grossTonnageParse.main(link)
	browser.quit()

if __name__ == '__main__':
    main()


