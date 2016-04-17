#!/usr/bin/python
#-------------------------------------------------
# rumahdijual.py
# (c) Jansen A. Simanullang
# 17.03.2016
# 18.03.2016 17:11
# 23.03.2016 18:01
# 17.04.2016 10:41 rumahdijual
#-------------------------------------------------
# BACKGROUND
# if you live in Indonesia and want to buy a house
# most likely you will visit: 'rumahdijual.com'
# in Bahasa 'rumahdijual' literally means 'house for sale'
#
# USAGE 
# python rumahdijual.py [area] [min] [max]
# [min] is minimum price in million (juta)
# [max] is maximum price in million (juta)
# example:
# python rumahdijual.py bogor 100 1000
# python rumahdijual.py depok 100 2000
#
# FEATURES
# * slow but sure crawler, avoid IP blocking
# * random select fetching method
# * direct fetch or via web proxy
# * random select web proxy
# * random select user agent
# * disable images in Chrome
# * limit search result criteria
# * sound of spinning coin after a page processed
# * phantom (invisible) mode support
#
# CONFIGURATION
# * config file:
# * number of pages to crawl
# * number of visited url
# * crawling resume from last visit
# * minimum price
# * maximum price
#
# OUTPUT 
# csv file of selected area located in OUTPUT folder
# you will able to sort and analyze the data
# for the best decision in buying a house
# 
# ALL RIGHTS RESERVED
# this script is provided as is without warranty to fit particular purpose or merchantability of any kind
# 
# If you make money from this script, please consider to make a donation!
# My family needs a house.
# jansen.simanullang@gmail.com
#---------------------------------------

from BeautifulSoup import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import base64, math, os, sys, time, urllib2, pyaudio, wave
from random import randint
from ConfigParser import SafeConfigParser

alamatURL = "http://rumahdijual.com/"
configName = 'resume.ini'
defaultAREA = "depok"
defaultMinprice = 100000000
defaultMaxprice = 2000000000
disableImage = True
phantomMode = True
# set phantom mode to True, to make the crawling invisible
# When phantomMode set to False, the crawling will be visible
	
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + os.sep
fullConfigName = scriptDirectory + configName

def clearScreen():

	if os.name == "posix":
		
		os.system("clear")

	else:
		
		os.system("cls")

		
def readConfig(area, option):
	#
	# read config file for last visit

	parser = SafeConfigParser()
	parser.read(configName)

	if parser.has_section(area) == False:

		parser.add_section(area)
	
	options = parser.items(area)
	
	existence = False
	
	for item in options:
	
		if item[0] == option:
		
			existence += True
			
	defaultValue = {"visit":"0", "pages":"0", "minprice":str(defaultMinprice), "maxprice":str(defaultMinprice)}
	
	if existence == False:
	
		parser.set(area, option, defaultValue[option])
	
		with open (r'resume.ini', 'wb') as configfile:
				
			parser.write(configfile)
			
	value = parser.get(area, option)
	
	return value
	

	
def updateConfig(area, option, value):
	#
	# update config file upon subprocess

	if not os.path.isfile(fullConfigName):

		print "create file"
		
	if os.path.isfile(fullConfigName):

		parser = SafeConfigParser()
		parser.read(configName)

		if parser.has_section(area) == False:

			parser.add_section(area)
			
		parser.set(area, option, value)
			
		with open (r'resume.ini', 'wb') as configfile:

			parser.write(configfile)


		
def argCheck():

	flagChange = False

	if len(sys.argv) > 0:

		try:
		
			AREA = sys.argv[1]
			
		except IndexError:
		
			AREA = defaultAREA
			
		try:
		
			minPRICE = str(int(sys.argv[2])*1000000)
			before = readConfig(AREA, 'minprice')
			updateConfig(AREA, 'minprice', minPRICE)
			after = readConfig(AREA, 'minprice')
			
			if before != after:
				flagChange += True
		
		except:
		
			minPRICE = readConfig(AREA, 'minprice')
			
		try:
		
			maxPRICE = str(int(sys.argv[3])*1000000)
			before = readConfig(AREA, 'minprice')
			updateConfig(AREA, 'maxprice', maxPRICE)
			after = readConfig(AREA, 'minprice')

			if before != after:
				flagChange += True
				
		except:
		
			maxPRICE = readConfig(AREA, 'maxprice')
			
	if flagChange == True:
	
		# if arguments changed then reset 'visit' and 'pages'
	
		updateConfig(AREA, 'visit', '0')
		updateConfig(AREA, 'pages', '0')


	return AREA, minPRICE, maxPRICE


AREA, minPRICE, maxPRICE = argCheck()


def pickUserAgent():
  #
  # randomly picks user agent for crawlers
  #------------------------------------------

	customUserAgent =['Chilkat/1.0.0 (+http://www.chilkatsoft.com/ChilkatHttpUA.asp)','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A342 Safari/601.1','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36','Chilkat/1.0.0 (+http://www.chilkatsoft.com/ChilkatHttpUA.asp)','Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 640 XL)','Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 640 XL','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36']
	
	userAgent = customUserAgent[randint(0,len(customUserAgent)-1)]

	return userAgent
	
	

def directFetch(alamatURL):
	# fungsi ini hanya untuk mengambil stream string HTML dari alamat URL yang akan dimonitor
	# Content-Type utf-8 raises an error when meets strange character
	#print "fetching HTML from URL...\n", alamatURL
	
	
	try:
	
		userAgent = pickUserAgent()

		strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': userAgent})).read()

		strHTML = strHTML.decode("windows-1252")

		strHTML = strHTML.encode('ascii', 'ignore')

		mysoup = BeautifulSoup(strHTML)
		
		#print ">> URL fetched."
		
	except:
		
		print "\nwaiting... (if the problem persists try disconnecting and reconnecting your connection without closing this window)"
		time.sleep(1)
		strHTML = proxyFetch(alamatURL)
		
	return strHTML



def getLastPage(strHTML):
  #
  # get the number of pages to crawl
  #------------------------------------------
	
	soup = BeautifulSoup(strHTML)
	pagenav = soup.findAll('td', {"class":"tcat"})[1]
	searchresult =  pagenav.getText().split('dari')[1].replace(")","").strip()
	pages = int(math.ceil(int(searchresult)/15.0))
	return int(pages)
	
	
	
def getDatafromPage(strHTML):
  #
  # get data and dump to csv file
  #------------------------------------------
	
	soup = BeautifulSoup(strHTML)
	
	scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
	
	fullPath = scriptDirectory + "OUTPUT/"
	outputfile = fullPath + AREA + "-between-"+str(int(minPRICE)/1000000)+"-"+str(int(maxPRICE)/1000000)+".csv"

	if not os.path.exists(fullPath):
		os.mkdir(fullPath)
		os.chdir(fullPath)

	if not os.path.isfile(outputfile):

		fileCreate(outputfile, "harga, tanah, bangunan, tidur, mandi, url\n")
		
		
  # get the premium advertised content
  
	resultset = soup.findAll('table', {"class":"tblSearchResultRow tblPremiumClass"})
	
	for result in resultset:
						
		tdset = result.findAll('td')
						
		for td in tdset:

			try:
							
				if td['class'] == 'tdInfoSpec':
								
					data = td.getText()
					data = str(formatData(cleanUpText(data))).strip("()")
					
						
				if td['class'] == 'TdTitleDesc':
								
					strURL = td.find('a')['href']
					
						
			except:
							
				continue
		
		strURL = correctURL(strURL)
							
		data = data + ", " + strURL

		fileAppend(outputfile, data+"\n")
		
	# get the forum content
	
	resultset = soup.findAll('table', {"class":"tblSearchResultRow"})

	for result in resultset:
	
		tdset = result.findAll('td')
						
		for td in tdset:

			try:
							
				if td['class'] == 'tdInfoSpec':
								
					data = td.getText()
					data = str(formatData(cleanUpText(data))).strip("()")
					
						
				if td['class'] == 'TdTitleDesc':
								
					strURL = td.find('a')['href']
					
						
			except:
							
				continue
								

		strURL = correctURL(strURL)
							
		data = data + ", " + strURL

		fileAppend(outputfile, data+"\n")

	
			

def cleanUpText(strText):
  #
  # add space for clarity
  # remove extra white space

	strText = 	strText.replace("juta"," juta")
	strText = 	strText.replace("juta","juta ")
	

	strText = 	strText.replace("miliar","miliar ")
	strText = 	strText.replace("miliar"," miliar")
	strText = 	strText.replace("m2","m2 ")
	strText = 	strText.replace("tanah", "tanah ")
	strText = 	strText.replace("bangunan", "bangunan ")
	
	strText = 	strText.replace("&nbsp;"," ")
	
	while "  " in strText:
	
		strText =	strText.replace("  "," ")

	return strText
	
	
	
def formatData(strText):
  #
  # format data

	strText = strText.split(" ")
	
	try:
		shiftIndex = 0
		if "juta" in strText:
			harga = 	int(strText[0])
		elif "miliar" in strText:
			harga = 	int(float(strText[0])*1000)
		else:
			harga = None
			shiftIndex = -2
	except:
	
		harga = None
		shiftIndex = -2
		
	try:
		tanah = None
		tanah = int(strText[2+shiftIndex])
	except:
		tanah = None
	try:
		bangunan = int(strText[5+shiftIndex])
	except:
		bangunan = None
	try:
		tidur = int(strText[8+shiftIndex])
	except:
		tidur = None
	try:	
		mandi = int(strText[9+shiftIndex])
	except:
		mandi = None
		if (tidur != None) and (len(str(tidur)) > 1):
			mandi = int(str(tidur)[-1])
			tidur = int(str(tidur)[0])
		
	return harga, tanah, bangunan, tidur, mandi
	
	
	
def fileCreate(strNamaFile, strData):
	#--------------------------------
	# fileCreate(strNamaFile, strData)
	# create a text file
	#
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()
	
	
	
def fileAppend(strNamaFile, strData):
  #
  # append data to output file
	try:
		f = open(strNamaFile, "a")
		f.writelines(str(strData))
		f.close()
	except:
		print "The file is being used in another process. Please close the file and retry..."
		fileAppend(strNamaFile, strData)


		
def proxyFetch(alamatURL):
	#
	# fetch web page via web proxy

	webProxy = pickProxy()
	
	try:
	
		
		if phantomMode:
		
			browser = Browser('phantomjs')
	
		else:
			
			try:
				# preferably using Chrome
				browser = Browser('chrome')
				
				if disableImage == True:
				
					browser.driver.close()

					options = webdriver.ChromeOptions()
					options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
					options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
					browser.driver = webdriver.Chrome(chrome_options=options)
			
			except:
				# "please install Chrome Web Driver from https://sites.google.com/a/chromium.org/chromedriver/downloads"
				browser = Browser()
		
		browser.driver.maximize_window()

		browser.visit(webProxy)
		
		time.sleep(2)

		browser.fill('u', alamatURL)
		
		divs = browser.find_by_value('Go').first.click()
		
		time.sleep(10)
		
		strHTML = browser.html

		# uncomment this if you want to print HTML source to screen
		#strHTML = strHTML.encode('ascii', 'ignore').decode('ascii')
		#print strHTML
		
		browser.driver.close()
		
	except:
	
		try:
			browser.driver.close()
		except:
			pass
			
		print "retrying..."
		
		strHTML = switchFetch(alamatURL)
	
	return strHTML
	
	
	
def pickProxy():

	#
	# random select proxy to use
	
	prox = {}
	prox['1'] = range(1,9)
	prox['2'] = range(1,4)
	prox['3'] = range(1,4)
	prox['4'] = range(1,4)
	prox['5'] = range(1,2)
	prox['6'] = range(1,2)
	prox['7'] = range(1,2)
	
	randKey = str(randint(1,len(prox)-1))
	
	if len(prox[randKey])>1:

		randIdx = randint(1, len(prox[randKey])-1)
		
	else:
	
		randIdx = 1
	
	webProxy = "https://"+str(randKey)+".hidemyass.com/ip-"+ str(randIdx)
	
	return webProxy
	
	
	
def decodeURL(strURL):
  #
  # return decoded URL encoded after proxy

	try:

		strURL = strURL.split("/")[-1]
		strURL = urllib2.unquote(strURL)
		strURL = strURL.decode('base64')
		strURL = "http" + strURL

	except:
	
		print strURL

	return strURL
	
	
def switchFetch(alamatURL):

	randKey = randint(1,2)
	
	if randKey == 1:
		
		#print "try connecting directly...\r\n"
		#print "try pressing ENTER here if not responding...\r\n"

		
		strHTML = directFetch(alamatURL)
		
	else:
		
		#print "try connecting via web proxy...\r\n"
		#print "try closing browser if browser not responding...\r\n"
		
		strHTML = proxyFetch(alamatURL)
		
	return strHTML
	
	
def correctURL(strURL):
  #
  # add main domain if necessary
  # decode only the encoded URL

	if ("http" not in strURL) and ("https" not in strURL):
	
		strURL = "http://rumahdijual.com/" + AREA + "/"+ strURL
		
	if "rumahdijual.com" not in strURL:
		
		strURL = decodeURL(strURL)
		
	return strURL
	
	

def playWav(filename):

	CHUNK = 1024

	wf = wave.open(filename, 'rb')

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	data = wf.readframes(CHUNK)

	while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	p.terminate()
	
	

def crawl(AREA, minPRICE, maxPRICE):
	
	alamatURL = "http://rumahdijual.com/carirumah.php?transaksi=BELI&jenis=RUMAH&kota="+AREA+"&minprice="+minPRICE+"&maxprice="+maxPRICE
	
	clearScreen()
	
	pages = readConfig(AREA, 'pages')
	
	if (int(pages) == 0):
	
		msgBody = switchFetch(alamatURL)
		
		pages = getLastPage(msgBody)
		
		updateConfig(AREA, 'pages', str(pages))
		
	pages = readConfig(AREA, 'pages')
	
	visit = readConfig(AREA, 'visit')

	for i in range(int(visit)+1, int(pages)+1):
	
		cursorURL = alamatURL = "http://rumahdijual.com/carirumah.php?sort=2&transaksi=BELI&jenis=RUMAH&kota="+AREA+"&minprice="+minPRICE+"&maxprice="+maxPRICE+"&p="+str(i)
		
		clearScreen()
		
		sys.stdout.write("fetching data from:\n"+ cursorURL+ "...\n page: "+str(i)+" of " +str(pages) + " pages")
	
		msgBody = switchFetch(cursorURL)
		
		getDatafromPage(msgBody)
		
		updateConfig(AREA, 'visit', str(i))
		
		visit = readConfig(AREA, 'visit')
		
		sys.stdout.write(" fetched...")
		
		playWav(scriptDirectory+os.path.join("wav","spinning-coin-1.wav"))
		
		sys.stdout.flush()

		if int(i) == int(pages):
		
			sys.stdout.write("\n FETCHING PROCESS FINISHED.\n\n Please check OUTPUT folder.\n Output written as file: " + AREA + "-between-" + str(int(minPRICE)/1000000)+"-"+str(int(maxPRICE)/1000000)+".csv\n\n HAVE A NICE DAY! GOD BLESS YOU!\n\n")
			
			os.remove(scriptDirectory+"resume.ini")
			
			playWav(scriptDirectory+os.path.join("wav","burp-1.wav"))

	
# below are the main lines of this script
crawl(AREA, minPRICE, maxPRICE)
