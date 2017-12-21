# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from Crawler.items import Product
from Crawler.loaders import HipHoperLoader


class HiphoperSpider(scrapy.Spider):
    name = 'hiphoper'
    allowed_domains = ['hiphoper.com']
    start_urls = ['http://www.hiphoper.com/shop/list.php?ca_id=AA',
                  'http://www.hiphoper.com/shop/list.php?ca_id=BB', ]
    
    item_fields = {
        'title': '//div[@id="info-wrap"]/p[@class="name"]/text()',
        'thumbnail': '//img[@id="zoom_03"]/@src',
        'price': '//div[text()[contains(., "정가")]]/following-sibling::span/text()',
        'originalCategory': '//ul[@class="breadcrumb"]/li/a/text()',
        'brand': '//div[text()[contains(., "브랜드")]]/following-sibling::span/text()',
        'detailImages': '//div[@id="product-detail"]//img/@src',
        'description': '//div[@id="product-detail"]//text()',
        'detailHtml': '//div[@id="product-html"]',
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_paging)
    
    def parse_paging(self, response):
        limit = int(response.xpath('//a[text()[contains(.,"Last")]]/@href').re('\d+$')[0])
        for page_no in range(1, limit):
            yield scrapy.Request(response.url+'&page={}'.format(page_no), callback=self.parse_list)
    
    def parse_list(self, response):
        item_links = response.xpath('//div[@class="imgwrap"]/a/@href').extract()
        for url in item_links:
            yield scrapy.Request(url, callback=self.parse_item)
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
                   with this docstring.

                   @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
                   @returns items 1 16
                   @returns requests 0 0
                   @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
                   """
        loader = HipHoperLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        
        product_no_obj = re.findall('[a-zA-Z]\d+', response.url)
        if product_no_obj:
            loader.add_value('productNo', product_no_obj[0])
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        
        label_regex = '.+,\d+,\d+|\W+|option|value|nbsp|0원|선택|품절|사이즈'
        if response.xpath('//select[@id="it_option_2"]'):
            url = "http://www.hiphoper.com/shop/itemoption.php"
            data = {'it_id': product_no_obj[0]}
            res = requests.post(url=url, data=data)
            tag_data = re.split('\n', res.text)
            size_labels = [re.sub(label_regex, '', option) for option in tag_data]
        else:
            size_labels = response.xpath('//select[@id="it_option_1"]/option/text()').extract()
            size_labels = [re.sub(label_regex, '', label) for label in size_labels]
        
        loader.add_value('originalSizeLabel', size_labels)
        
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
