# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 21:37:35 2016

@author: Elena
"""

from lxml import html
import requests
from urllib import urlretrieve 

def get_info_from_filmup(film_url):
	page = requests.get(film_url)
	tree = html.fromstring(page.content)

	#Fetch the infos as a list:
	info = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/tr/td/font/text()')
	plot = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/font/text()')
	image = tree.xpath('//div[@id="container"]/table/tr/td/div/table/tr/td/table/tr/td/table/form/tr/td/a[@class="filmup"]/@href')

	#print(image[0])
	#Fetch large image url
	image_page = requests.get('http://filmup.leonardo.it/'+image[0])
	tree = html.fromstring(image_page.content)

	image_big = tree.xpath('//div[@id="container"]/table/tr/td/div/div/img/@src')
		
	#Download image in local folder
	urlretrieve('http://filmup.leonardo.it'+image_big[0], "images/loc.jpg")
	#print(image downloaded)
	return 'http://filmup.leonardo.it'+image_big[0]

