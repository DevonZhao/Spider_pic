#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os,urllib

import scrapy
import requests

from tutorial.items import MeizituSpiderItem

next_page_link = []

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
}


def dowanload_pic(url):
	first_name = url[-18:]
	path = "/Users/devon/Python/meizitu/"
	name = path+first_name.replace('/','_')
	r = requests.get(url, headers=headers)
	if not os.path.exists(name):
		with open(name, "wb") as code:
			code.write(r.content)
	else:
		print 'this pic exists error .........'
		pass

class meizitu_spider(scrapy.Spider):
	"""docstring for meizitu_spider"""
	name = "meizitu_spider"
	start_urls = ["http://www.meizitu.com/tag/qizhi_53_1.html"]
	allow_urls = ["meizitu.com"]

	def parse(self,response):
		for href in response.xpath("//ul[@class='wp-list clearfix']/li/div/div/a/@href").extract():
			yield scrapy.Request(href,callback=self.parse_picture)

		pages_link = response.xpath("//div[@id='wp_page_numbers']/ul/li/a/@href").extract()
		full_page_link = "http://www.meizitu.com/"+pages_link[-2]
		if full_page_link not in next_page_link:
			yield scrapy.Request(full_page_link,callback=self.parse)
		else:
			print "I finished everthing but I can't exit by myself, so please enter 'ctrl+c' to quit, thank you"



	def parse_picture(self,response):
		item  = MeizituSpiderItem()
		item['pic_name'] = response.selector.xpath("//title/text()").extract()
		item['pic_url'] = response.selector.xpath("//div/p/img/@src").extract()
		yield item
		for url in item['pic_url']:
			dowanload_pic(url)