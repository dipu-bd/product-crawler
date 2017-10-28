# -*- coding: utf-8 -*-
"""
Use `scrapy crawl products` to run this spider
"""
import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProductsSpider(CrawlSpider):
    """Crawl all products"""
    name = 'products'
    allowed_domains = ['www.daraz.com.bd']
    start_urls = ['http://www.daraz.com.bd/']

    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    primary_key = 'link'
    collection_name = 'daraz'

    def parse_item(self, response):
        """Parse products from page"""
        if response.url[-5:] != '.html':
            logging.info('Skipped: %s', response.url)
            return
        # end if
        logging.info('Parsing: %s', response.url)

        item = dict()
        item['link'] = response.url

        main = response.css('main.osh-container')
        category = main.xpath('.//nav//a/@title').extract()
        item['category'] = category[1:-1]
        item['title'] = category[-1]

        item['features'] = main.css('.list.-features ul li::text').extract()

        ######################### Main Information #########################

        detail = main.css('section.sku-detail')
        item['previews'] = detail.css('#thumbs-slide').xpath('.//@href').extract()

        brand = detail.css('a.brand')
        item['brand'] = {
            'name': brand.xpath('./img/@alt').extract_first(),
            'logo': brand.xpath('./img/@src').extract_first()
        }

        item['title'] = detail.css('h1.title::text').extract_first() or item['title']


        price_box = detail.css('div.price-box')
        price = price_box.css('span.price:not(.-old)')
        old_price = price_box.css('span.price.-old')
        item['price'] = {
            'value': price.xpath('.//span/@data-price').extract_first(),
            'currency': price.xpath('.//span/@data-currency-iso').extract_first(),
        }

        if len(old_price) > 0:
            item['old_price'] = {
                'value': old_price.xpath('.//span/@data-price').extract_first(),
                'currency': old_price.xpath('.//span/@data-currency-iso').extract_first(),
            }
            item['discount_rate'] = price_box.css('.sale-flag-percent::text').extract_first()
        # end if

        item['warranty'] = detail.css('.-warranty .-description::text').extract_first("Not Specified")

        ######################### Extra Descriptions #########################

        tabs = main.css('div.osh-tabs')
        item['description'] = tabs.css('.product-description').extract_first()

        item['specs'] = dict()
        for spec in tabs.css('div.osh-table div.osh-row'):
            key = spec.css('.osh-col.-head::text').extract_first()
            val = spec.css('.osh-col:not(.-head)::text').extract_first()
            if key and val:
                item['specs'].update({key: val})
            # end if
        # end for

        item['rating'] = tabs.css('#ratingReviews .avg span::text').extract_first()

        yield item
    # end def
# end def

"""
Traits
--------------
- Product page usually ends with .html
- `main.osh-container` is the our ROI
- `nav.osh-breadcrumb ul` contains categories. Last is Product name. Take [1:-1]
- `section.sku-detail` contains details
- `div.media div#thumbs-slide a::attr(href)` has the
- `div.detail-features ul li::text` has feature list. Removing non-ascii code is recommended.
- `span.price:not(.-old)` selects current price
- `span.price.-old` selects old price
- sometime description contains specification
- key features are seen in 3 places: main details section, description tab, specifications tab.
"""
