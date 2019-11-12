import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import urllib.request, urllib.parse, urllib.error
import ssl
import time
import openpyxl
from fake_useragent import UserAgent

def get_proxy_html(http_only=False):
	'''
	Function
    ---------------------
	Gets http response from free proxy site 'https://free-proxy-list.net/#'.
    ---------------------

	Inputs
    ---------------------
    http_only : only return HTTP proxies, or both HTTP and HTTPS
    ---------------------
	'''
	url = 'https://free-proxy-list.net/#'
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}

	request = urllib.request.Request(url, headers=hdr)

	response = urllib.request.urlopen(request, context=ctx)
	html = response.read().decode('utf-8')

	return html

def get_us_proxy_list(http_only=False):
	'''
	Function
    ---------------------
	Returns list of IPs from free proxy site 'https://free-proxy-list.net/#'.
    ---------------------

	Inputs
    ---------------------
    http_only : only return HTTP proxies, or both HTTP and HTTPS
    ---------------------
	'''
	html = get_proxy_html(http_only=http_only)

	soup = BeautifulSoup(html, 'html.parser')
	tbl_ips = soup.find('table', {'id': 'proxylisttable'})
	ips_us = []

	for tr in tbl_ips.find('tbody').find_all('tr'):
		tds = tr.find_all('td')

		if tds[2].text == 'US':
			if http_only:
				if tds[6].text == 'no':
					ips_us.append('http://' + tds[0].text)
			else:
				ips_us.append('http://' + tds[0].text)

	return ips_us

if __name__ == '__main__':
	# proxy_list = get_us_proxy_list(http_only=False)
	proxy_list_html = get_proxy_html(http_only=True)
	proxy_list_http = get_us_proxy_list(proxy_list_html)

	print(proxy_list_http)
