# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 21:37:35 2016

@author: Elena
"""

from lxml import html
import requests
from urllib import urlretrieve 
import re
import PIL
from PIL import Image

def resize_image(image,width=0, height=0):
	basewidth = 300
	if width!=0:
		wpercent = (width / float(image.size[0]))
		hsize = int((float(image.size[1]) * float(wpercent)))
		image = image.resize((width, hsize), PIL.Image.ANTIALIAS)
	else:
		hpercent = (height / float(image.size[1]))
		wsize = int((float(image.size[0]) * float(hpercent)))
		image = image.resize((wsize, height), PIL.Image.ANTIALIAS)
	return image

def get_text(el):
	if isinstance(el, basestring):
		return el
	else:
		if len(el.xpath('text()'))>0:
			return el.xpath('text()')[0]
		else:
			return ""

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

def substitue_accents(s):
	s = re.sub(r'\à',"a'",s)
	s = re.sub(r'\ù',"u'",s)
	s = re.sub(r'\ò',"o'",s)
	return re.sub(r'ì',"i''",s)

def get_info_from_filmup(film_url):
	page = requests.get(film_url)
	tree = html.fromstring(page.content)

	#Fetch the infos as a list:
	info = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/tr/td/font/node()')
	print len(info)
	info = [get_text(i) for i in info]
	plot = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/font/text()')
	image = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/form/tr/td/a[@class="filmup"]/@href')
	plot[1] = parse_apostrophe(plot[1])
	plot[1] = substitue_accents(plot[1])
	
	#Fetch large image url
	image_page = requests.get('http://filmup.leonardo.it/'+image[0])
	tree = html.fromstring(image_page.content)
	
	image_big = tree.xpath('//div[@id="container"]/table/tr/td/div/div/img/@src')

	#Download image in local folder
	s = r'/sc_(.[^\.]*)\.htm'
	#print re.findall(s,film_url)
	img_title = "images/"+re.findall(s,film_url)[0]+".jpg"
	urlretrieve('http://filmup.leonardo.it'+image_big[0], img_title)
	#resize image:
	image = Image.open(img_title)
	image_small = resize_image(image,height=330)
	image_small.save("images/"+re.findall(s,film_url)[0]+"_small.jpg")
	image_fullsize = resize_image(image,height=600)
	image_fullsize.save("images/"+re.findall(s,film_url)[0]+".jpg")
	
	res = merge_infos(info, plot)
	
	return res