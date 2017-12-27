# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from scrapy_splash import SplashRequest
from Crawler.items import Product
from Crawler.loaders import A29CMLoader


class A29cmSpider(scrapy.Spider):
    name = '29cm'
    allowed_domains = ['29cm.co.kr']
    start_urls = ['http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=51',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=52',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=53',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=54',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=55',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=56',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=57',
                  'http://www.29cm.co.kr/shop/shop.asp?&selS=24&MCC=58',
                  ]
    
    item_fields = {
        'title': '//div[@class="name"]/text()',
        'thumbnail': '//div[@class="i-container"]/img/@src',
        'price': '//div[@class="o"]/text() | //div[@class="price"]/text()',
        'salePrice': '//div[@class="s"]/text()',
        'originalCategory': '//nav[@id="cateNav"]/ul/li/a/text()',
        'brand': '//h1[@class="h1-B"]/text()',
        'productNo': '//span[text()[contains(.,"Code")]]/following-sibling::span/text()',
        'detailImages': '//div[@class="item-Detail"]//img/@src',
        'description': '//div[@class="item-Detail"]//text()',
        'detailHtml': '//div[@class="item-Detail"]',
    }
    
    custom_settings = {
        'SPLASH_URL': os.environ['SPLASH_URL'],
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse_paging, args={'wait': 10.0})
    
    def parse_paging(self, response):
        limit = response.xpath('//div[@class="pagination"]/ul/li/a/@data-ic').extract()[-2]
        for i in range(1, limit):
            yield SplashRequest(response.url + "&iC={}".format(i), callback=self.parse_list, args={'wait': 3})
            
    def parse_list(self, response):
        item_links = response.xpath('//a[@href[contains(.,"idx=")]]/@href').extract()
        for link in item_links:
            yield SplashRequest('http://www.29cm.co.kr'+link, callback=self.parse_item, args={'wait': 3})
            
    def parse_item(self, response):
        loader = A29CMLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        url = "https://cache.29cm.co.kr/app/v3/shop/productOption.asp?idx={}".format(loader.load_item()['productNo'])
        res = requests.get(url=url)
        res = res.json()
        if 'list' in res['option']:
            size_labels = [obj['title'] for obj in res['option']['list']]
        else:
            size_labels = None
        loader.add_value('originalSizeLabel', size_labels)
        loader.add_value('shopHost', self.name)
        loader.add_value('url', response.url)
        
        return loader.load_item()
        
        
    