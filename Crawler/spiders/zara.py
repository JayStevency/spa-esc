# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.loaders import ZaraLoader
from Crawler.items import Product


class ZaraSpider(CrawlSpider):
    name = 'zara'
    allowed_domains = ['www.zara.com']
    
    start_urls = ['https://www.zara.com/kr/']
    
    item_fields = {
        'title': '//h1[@class="product-name"]/text()',
        'productNo': '//img/@data-id',
        'thumbnail': '//div[@class="media-wrap image-wrap"]/a/@href',
        'salePrice': '//empty',
        'originalSizeLabel': '//span[@class="size-name"]/text()',
        'color': '//span[@class="_colorName"]/text()',
        'material': '//empty',
    }
    
    custom_settings = {
        'AJAXCRAWL_ENABLED': True
    }
    
    
    rules = (
        # Rule(LinkExtractor(allow=(r'.')), callback='parse_list'),
        Rule(LinkExtractor(allow=('man', 'woman', 'trf'), deny=(r'\?v1=11112', r'\?v1=18002', 'en')), follow=True),
        Rule(LinkExtractor(allow='\.html\?v1=\d+$', deny=(r'\?v1=11112', r'\?v1=18002', 'en')),
             follow=True),
        Rule(LinkExtractor(allow=r'v2=\d+$', deny=(r'\?v1=11112', r'\?v1=18002', 'en')), callback='parse_item'),
    
    )
    
    def parse_item(self, response):
        loader = ZaraLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        
        result = response.xpath('//script[text()[contains(., "window.zara.appConfig")]]/text()').extract_first()
        price_data = re.findall(r'price\"\:\d+', result)
        
        loader.add_value('price', price_data[0])
        
        category_no = re.findall(r'\d+$', response.url)[0]
        loader.add_xpath('originalCategory', '//li[@data-categoryid=%s]/a/text()' % category_no)
        
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
