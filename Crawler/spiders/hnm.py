# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.loaders import HnmLoader
from Crawler.items import Product


class HnmSpider(CrawlSpider):
    name = 'hnm'
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'http://www2.hm.com/ko_kr/ladies/shop-by-product/view-all.html?'
        'product-type=ladies_all&sort=stock&offset={}&page-size=100',
        'http://www2.hm.com/ko_kr/men/shop-by-product/view-all.html?'
        'product-type=men_all&sort=stock&offset={}&page-size=100',
        'http://www2.hm.com/ko_kr/sale/shopbyproductladies/view-all.html?'
        'product-type=ladies_all&sort=stock&offset={}&page-size=100',
        'http://www2.hm.com/ko_kr/sale/shopbyproductmen/viewall.html?'
        'product-type=men_all&sort=stock&offset={}&page-size=100'
    ]
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True
    }
    
    rules = (
        Rule(LinkExtractor(allow=r'ko_kr\/productpage\.\d+\.html'), callback='parse_item'),
    )
    
    def start_requests(self):
        for i in range(4):
            return [scrapy.Request(self.start_urls[i].format(j * 100)) for j in range(100)]
    
    def parse_item(self, response):
        loader = HnmLoader(item=Product(), response=response)
        data = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        data = json.loads(data)
        loader.add_value('title', data['name'])
        loader.add_value('color', data['color'])
        loader.add_value('thumbnail', data['image'])
        loader.add_value('originalCategory', data['category']['name'])
        loader.add_value('productNo', data['sku'])
        loader.add_value('description', data['description'])
        loader.add_xpath('originalSizeLabel',
                         '//ul[@data-sizelist=%s]/li[@class="list-item"]//span/text()' % data['sku'])
        loader.add_xpath('detailImages', '//*[@class="product-detail-thumbnails"]//img/@src')
        
        origin_price = response.xpath('//small[@class="price-value-original"]/text()').extract()
        if origin_price:
            loader.add_value('price', origin_price)
            loader.add_xpath('salePrice', '//span[@class="price-value"]/text()')
        else:
            loader.add_xpath('price', '//span[@class="price-value"]/text()')
        
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
