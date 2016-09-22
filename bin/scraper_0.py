# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 21:37:35 2016

@author: Elena
"""

from lxml import html
import requests
from urllib import urlretrieve 
import re

def get_text(el):
	if isinstance(el, basestring):
		return el
	else:
		return el.xpath('text()')[0]

def is_field(string):
	str_is_field = r'.*:\xa0'
	if len(re.findall(str_is_field,string))>0:        
		return True
	else:
		return False

def merge_infos(main_info, plot):    
	field_name = r'(.*):'
	fields = []
	values = []
	value = ''
	end = 0
	for i in main_info:
		if is_field(i):
			values += [value]
			value = ''
			fields += [re.findall(field_name,i)[0]]            
		else:
			value += i
	values += [value]
	fields += [re.findall(field_name,plot[0])[0]]
	values += [plot[1]]
	
	return dict(zip(fields,values[1:]))

def parse_apostrophe(s):
	s = re.sub(r'\x92',"\'",s)
	return re.sub(r'\x96',"-",s)

def get_info_from_filmup(film_url):
	page = requests.get(film_url)
	tree = html.fromstring(page.content)

	#Fetch the infos as a list:
	info = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/tr/td/font/node()')
	info = [get_text(i) for i in info]
	plot = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/font/text()')
	image = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/form/tr/td/a[@class="filmup"]/@href')
	plot[1] = parse_apostrophe(plot[1])
	
	#Fetch large image url
	image_page = requests.get('http://filmup.leonardo.it/'+image[0])
	tree = html.fromstring(image_page.content)
	
	image_big = tree.xpath('//div[@id="container"]/table/tr/td/div/div/img/@src')

	#Download image in local folder
	urlretrieve('http://filmup.leonardo.it'+image_big[0], "images/loc.jpg")
	#print(image downloaded)
	res = merge_infos(info, plot)
	return res