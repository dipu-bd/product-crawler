# -*- coding: utf-8 -*-
"""
Use `scrapy crawl products` to run this spider
"""
import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

LOG = logging.getLogger('Products')


class ProductsSpider(CrawlSpider):
    """Crawl all products"""
    name = 'products'
    allowed_domains = ['www.daraz.com.bd']
    start_urls = ['http://www.daraz.com.bd/']

    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """Parse products from page"""
        logging.info('Parsing: %s', response.url)
    # end def
# end def
