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
        is_item = response.url[-5:] == '.html'
        if not is_item:
            logging.info('Ignored: %s', response.url)
            return
        # end if
        logging.info('Parsing: %s', response.url)

        item = dict()
        item['link'] = response.url

        main = response.css('main.osh-container')
        breadcrumb = main.css('nav.osh-breadcrumb ul li a::text').extract()
        item['category'] = breadcrumb[1:-1]
        item['title'] = breadcrumb[-1]

        ######################### Main Information #########################
        detail = main.css('section.sku-detail')
        item['previews'] = detail.css('div.media div#thumbs-slide a::attr(href)').extract()
        item['brand'] = {
            'name': detail.css('a.brand img::attr(alt)').extract_first(),
            'logo': detail.css('a.brand img::attr(src)').extract_first(),
        }

        item['title'] = detail.css('h1.title::text').extract_first() or item['title']


        price_box = detail.css('div.price-box')
        price = price_box.css('span.price:not(.-old)')
        old_price = price_box.css('span.price:not(.-old)')
        item['price'] = {
            'value': price.css('span::attr(data-price)').extract_first(),
            'currency': price.css('span::attr(data-currency-iso)').extract_first(),
        }
        item['old_price'] = {
            'value': old_price.css('span::attr(data-price)').extract_first(),
            'currency': old_price.css('span::attr(data-currency-iso)').extract_first(),
        }

        item['discount_rate'] = price_box.css('span.sale-flag-percent::text').extract_first()

        item['warranty'] = detail.css('div.-warranty span.-description::text').extract_first()

        ######################### Extra Descriptions #########################
        tabs = main.css('div.osh-tabs')
        item['description'] = tabs.css('div.product-description').extract_first()

        item['features'] = main.css('.list.-features ul li::text').extract()

        item['specs'] = dict()
        for spec in tabs.css('div.osh-table div.osh-row'):
            key = spec.css('.osh-col.-head::text').extract_first()
            val = spec.css('.osh-col:not(.-head)::text').extract_first()
            if key and val:
                item['specs'].update({key: val})
            # end if
        # end for

        rating = tabs.css('div#ratingReviews .summary')
        item['rating'] = rating.css('.avg .container span::text').extract_first()

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
