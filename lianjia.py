#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import urllib
import os


class House(object):
	def __init__(self):
		self.where = None
		#self.region = None
		#self.zone = None
		#self.meters = None
		#self.direct = None
		self.price = None
		self.price_pre = None
		self.id = None
		self.url = None

	def show(self):
		return '%s %s  %s(%s)' % (self.id, self.where, self.price,
			self.price_pre)

class SpiderMain(object):
	def __init__(self, areas, room_num, brp, erp):
		# room_num: required number of rooms
		# brp: lowest price of house
		# erp: highest price of house

		self.root_url = "http://bj.lianjia.com/zufang/"
		self.constraint = 'l%dbrp%derp%drs' % (room_num, brp, erp)
		assert type(areas) == list
		self.areas = areas
		#print self.constraint
		#assert type(urls) == list
		#self.urls = urls
		self.result_urls = []

	def download(self, url):
		if url is None:
			return None
		try:
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(req)   # FIXME: add timeout
		except urllib2.HTTPError, e:
			print e.code
		except urllib2.URLError, e:
			print e.reason 
		else:
			if response.getcode() == 200:
				return response.read()
		return None

	def show_house_num(self, soup):
		tag = soup.find(class_= "list-head clear").find("span")
		house_num = tag.get_text()
		print "house_num: %s" % house_num
		return int(house_num)

	def list_house(self, soup):
		tag = soup.find(id="house-lst")
		data_list = tag.find_all('li')
		#print len(data_list)
		for data in data_list:
			house = House()
			house.id = data['data-id']
			house.where = data.find(class_='where').get_text()
			#house.region = data.find(class_='region').get_text()
			#house.zone = data.fild(class_='zone').get_text()
			#house.meters = data.find(class_='meters').get_text()
			house.price = data.find(class_='price').get_text()
			house.price_pre = data.find(class_='price-pre').get_text()
			print house.show()

	def parse_each_page(self, page_index, area):
		url = '%spg%d%s%s' % (self.root_url, page_index, self.constraint, area)
		#print 'url:',url
		html_cont = self.download(url)
		soup = BeautifulSoup(html_cont, 'lxml')
		self.list_house(soup)

	def parse(self, page_url, html_cont, area):
		if page_url is None or html_cont is None:
			return None
		#soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		soup = BeautifulSoup(html_cont, 'lxml')
		house_num = self.show_house_num(soup)
		page_num = (house_num + 29) / 30
		#print "page_num: %s" % page_num
		for page_index in range(1, page_num + 1):
			self.parse_each_page(page_index, area)


	def craw(self):
		for x in self.areas:
			area = urllib.quote(x)
			url = self.root_url + self.constraint + area
			html_cont = self.download(url)
			if html_cont == None:
				continue
			self.parse(url, html_cont, area)

		"""
		for url in self.urls:
			#print url
			html_cont = self.download(url)
			if html_cont == None:
				continue
			self.parse(url, html_cont)
		"""

if __name__ == "__main__":
	#root_url = "http://bj.lianjia.com/zufang/"
	#constraint = 'l2brp5500erp7500rs'
	areas = ['望京西园', '望京西园二区']
	#urls = map(lambda x:(root_url + constraint + urllib.quote(x)), areas)
	spider = SpiderMain(areas, 2, 5500, 10000)
	spider.craw()

