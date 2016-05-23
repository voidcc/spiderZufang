#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import urllib
import os

region_dict = {}

class House(object):
	def __init__(self):
		self.where = None
		self.region = None
		self.zone = None
		self.meters = None
		self.direct = None
		self.floor = None
		self.price = None
		self.price_pre = None
		self.id = None
		self.url = None

	def show(self):
		#return '%s %s %s' % (self.id, self.where, self.price)
		return u'%s %s平 %s %s %s %s' % (self.region, self.meters, self.zone,
				self.direct, self.floor, self.price)


class Spider_MaiTian(object):
	def __init__(self):
		# R2C6: Wangjing
		# S4:5000-8000
		# H2: two rooms
		# O2: south
		self.root_url = "http://www.maitian.cn"
		self.constraint = '/zfall/R2C6/S4/H2O2'
		#self.result_urls = []

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
		tag = soup.find(class_= "screening").find("p").find("span")
		house_num = tag.get_text()
		return int(house_num)

	def list_house(self, soup):
		tag = soup.find(class_="list_wrap")
		data_list = tag.find_all('li')
		#print len(data_list)
		for data in data_list:
			house = House()
			#house.id = data['data-id']
			data_list = data.find(class_='list_title')
			house.where = data_list.find(class_="short").get_text()
			house.region = house.where.split("\n")[1].strip().split(u'朝阳')[0]
			temp = map(lambda x: x.get_text(), data_list.find('p').find_all('span'))
			house.meters = temp[0]
			house.zone = u'%s室%s厅%s卫' % (temp[1], temp[2], temp[3])
			temp = map(lambda x: x.get_text(), data_list.find('p').find_all('label'))
			house.direct = temp[0]
			house.floor = '%s/%s' % (temp[2], temp[3])
			house.price = data.find(class_='the_price').find("span").get_text()
			temp = data_list.find("h1").find("a")['href']
			house.id = temp.split('/')[-1]
			house.url = self.root_url + temp.strip()

			if region_dict.get(house.region) is None:
				region_dict[house.region] = [house]
			else:
				region_dict[house.region].append(house)

			#print house.show()
			#house.price_pre = data.find(class_='price-pre').get_text()
			#house.url = data.find(class_="pic-panel").find('a')['href']
			#print house.show()

	def parse_each_page(self, page_index):
		url = '%s/PG%d' % (self.root_url + self.constraint, page_index)
		print 'url:',url
		html_cont = self.download(url)
		soup = BeautifulSoup(html_cont, 'lxml')
		self.list_house(soup)

	def parse(self, html_cont):
		if html_cont is None:
			return None
		#soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		soup = BeautifulSoup(html_cont, 'lxml')
		house_num = self.show_house_num(soup)
		#print "house_num: %d" % house_num
		page_num = (house_num + 9) / 10
		print "House_num: %d  Page_num: %d" % (house_num, page_num)
		for page_index in range(1, page_num + 1):
			self.parse_each_page(page_index)
		"""
		for k, v in region_dict:
			print k, len(v)
		"""
		for k in region_dict.keys():
			print
			print k, len(region_dict[k])
			for i in region_dict[k]:
				print i.show()

	def craw(self):
		html_cont = self.download(self.root_url + self.constraint)
		self.parse(html_cont)


if __name__ == "__main__":
	spider = Spider_MaiTian()
	spider.craw()

