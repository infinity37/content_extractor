#coding: utf-8
import bs4
import bs4.element
import re
import cgi
import urllib.request, urllib.error, urllib.parse
import requests
import math
import lxml
import sys

__all__ = ["BodyTextExtraction"]

ans = []
neg_words = ["nav", "menu", "foot", "btn", "image", "botton", "skip"]
def dfsdomtree(node, pre):
	if node.name != None:
		str1 = node.name.lower()
		for neg_word in neg_words: 
			if neg_word in str1:
				return

	try:
		str2 = str(node['class']).lower()
	except:
		str2 = ""
	else:
		for neg_word in neg_words: 
			if neg_word in str2:
				return
	try:
		str3 = str(node['id']).lower()
	except:
		str3 = ""
	else:
		for neg_word in neg_words: 
			if neg_word in str3:
				return

	try:
		str4 = str(node['role']).lower()
	except:
		str4 = ""
	else:
		for neg_word in neg_words: 
			if neg_word in str4:
				return

	try:
		for child in node.children:
			dfsdomtree(child,node)
	except AttributeError:
		strn = node.lower()
		for neg_word in neg_words: 
			if neg_word in strn:
				return
		if node != "":
			ans.append(node)
		return
	else:
		return

if __name__=="__main__":
	argvs = sys.argv

	url = argvs[1]
	f = open(url,'r',encoding='UTF-8')

	html_content = f.read()

	html_content = re.sub('(?is)<!DOCTYPE.*?>', '', html_content)
	html_content = re.sub('(?is)<!--.*?-->', '', html_content)  # remove html comment
	html_content = re.sub('(?is)<script.*?>.*?</script>', '', html_content)  # remove javascript
	html_content = re.sub('(?is)<style.*?>.*?</style>', '', html_content)  # remove css
	html_content = re.sub('(?is)<symbol.*?>.*?</symbol>', '', html_content)  # remove symbols
	html_content = re.sub('(?is)<header.*?>.*?</header>', '', html_content)  # remove header
	html_content = re.sub('(?is)<canvas.*?>.*?</canvas>', '', html_content)

	bsObj = bs4.BeautifulSoup(html_content, 'lxml')

	dfsdomtree(bsObj,None)
	for i in ans:
		if not i.isspace():
			print(i.strip())
