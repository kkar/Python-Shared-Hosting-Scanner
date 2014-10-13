#!/usr/bin/python

import socket, sys, re, urllib2, StringIO, gzip, zlib
from bs4 import BeautifulSoup
import tldextract

if len(sys.argv) <> 2:
	print '\n[!] Two arguments required.'
	print 'Example: python neighbs.py www.website.com'
	print 'Example: python neighbs.py 1.2.3.4'
	sys.exit()
else:
	sharedHost = sys.argv[1]
	duplicateCheckList = []

def validateHostIP(target):
	isIP = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", target)
	isHostName = re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", target)
	if isIP:
		return 'IP'
	elif isHostName:
		return 'HOSTNAME'
	else:
		return False

def resolve(target):
	if hasattr(socket, 'setdefaulttimeout'):
		socket.setdefaulttimeout(3)
	try:
		peos = socket.gethostbyaddr(target)
		return peos[2][0]
	except:
		return False

def make_requests(sharedTarget):
	response = [None]
	responseText = None

	for requests in range (1, 101):
		if(request_www_bing_com(response, requests, sharedTarget)):
			responseText = read_response(response[0])
			soup = BeautifulSoup(responseText)
			for A in soup.find_all('a', href=True):
				domain = str('.'.join(list(tldextract.extract(A['href']))[:10]))
				if not domain.startswith('.') and not len(domain) < 4:
					if domain not in duplicateCheckList:
						if resolve(sharedHost) == resolve(domain):
							duplicateCheckList.append(domain)
							print '[+] '+domain
				domain = ''
			
			response[0].close()

def read_response(response):
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO.StringIO(response.read())
		return gzip.GzipFile(fileobj=buf).read()

	elif response.info().get('Content-Encoding') == 'deflate':
		decompress = zlib.decompressobj(-zlib.MAX_WBITS)
		inflated = decompress.decompress(response.read())
		inflated += decompress.flush()
		return inflated

	return response.read()

def request_www_bing_com(response, requests, sharedTarget):
	response[0] = None
	try:
		req = urllib2.Request("http://www.bing.com/search?q=ip%3A"+str(sharedTarget)+"&first="+str(requests))

		req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0")
		req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		req.add_header("Accept-Language", "en-US,en;q=0.5")
		req.add_header("Accept-Encoding", "gzip, deflate")
		req.add_header("Referer", "http://www.bing.com/")
		req.add_header("Cookie", "_EDGE_V=1; MUID=1A8733283AE36E853EB935873BA66FEF; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DF63C8A66FB64714818DCF4DFC12DEE1; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20140908; MUIDB=1A8733283AE36E853EB935873BA66FEF; SRCHHPGUSR=CW=1280&CH=887; _RwBf=s=70&o=16; _HOP=; _SS=SID=BCC8BCA1D49C412281A16C56834A77B5&bIm=819187; SCRHDN=ASD=0&DURL=#; WLS=TS=63547515929")
		req.add_header("Connection", "keep-alive")

		response[0] = urllib2.urlopen(req)

	except urllib2.URLError, e:
		if not hasattr(e, "code"):
			return False
		response[0] = e
	except:
		return False

	return True

print '\n[*] Scanning for shared hosts. Please wait...'
print '------------------------------------------------'
if validateHostIP(sharedHost) == 'IP':
	make_requests(sharedHost)
elif validateHostIP(sharedHost) == 'HOSTNAME':
	make_requests(resolve(sharedHost))
else:
	print 'Something went wrong. Try again.'
print '------------------------------------------------'
print '[*] '+str(len(duplicateCheckList))+' unique domains found and verified to be on the same server.'
