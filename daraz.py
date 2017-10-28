# -*- coding: utf-8 -*-
import scrapy


class DarazSpider(scrapy.Spider):
    name = 'daraz'
    allowed_domains = ['daraz.com']
    start_urls = ['http://daraz.com/']

    def parse(self, response):
        pass
