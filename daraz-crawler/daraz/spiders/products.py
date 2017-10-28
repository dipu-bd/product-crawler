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

    def parse_item(self, response):
        """Parse products from page"""
        is_item = response.url[-5:] == '.html'
        if not is_item:
            logging.info('Ignored: %s', response.url)
            return
        # end if
        logging.info('Parsing: %s', response.url)

        item = dict()
        main = response.css('main.osh-container')

        breadcrumb = main.css('nav.osh-breadcrumb ul li a::text').extract()
        item['category'] = breadcrumb[1:-1]
        #item['title'] = breadcrumb[-1]

        #################################### Main Information ####################################

        detail = main.css('section.sku-detail')
        item['previews'] = detail.css('div.media div#thumbs-slide a::attr(href)').extract()
        item['brand'] = {
            'name': detail.css('a.brand img::attr(alt)').extract_first(),
            'logo': detail.css('a.brand img::attr(src)').extract_first(),
        }

        item['title'] = detail.css('h1.title::text').extract_first()

        features = detail.css('div.detail-features ul li::text').extract()
        item['features'] = [x.encode('ascii', 'ignore').decode('utf8') for x in features]

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

        item['discount_percent'] = price_box.css('span.sale-flag-percent').extract_first()

        item['warranty'] = detail.css('div.-warranty span.-description::text').extract_first()

        #################################### Extrac Descriptions ####################################

        


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

"""
