# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from Crawler.items import Product
from Crawler.loaders import MusinsaLoader


class MusinsaSpider(scrapy.Spider):
    name = 'musinsa'
    allowed_domains = ['store.musinsa.com']
    category_nums = [('001', 600), ('002', 150), ('003', 150), ('020', 20), ('007', 150), ('008', 40), ('011', 200)]
    start_urls = ['http://store.musinsa.com/app/items/lists/{}'.format(i[0]) for i in category_nums]
    
    item_fields = {
        'title': '//span[@class="product_title"]/span[not(@class)]/text()',
        'thumbnail': '//*[@class="product-img"]/img/@src',
        'price': '//span[@id="goods_price"]/*/text() | //span[@id="goods_price"]/text()',
        'salePrice': '//span[@id="sale_price"]/text()',
        'material': '//li[text()[contains(.,"소재")]]/following-sibling::li/text()',
        'originalCategory': '//*[@class="item_categories"]/a/text()',
        'brand': '//*[@class="brand"]/a/span/text()',
        'detailImages': '//div[@class="detail_product_info"]//img/@src',
        'description': '//div[@class="detail_product_info"]//text()',
        'detailHtml': '//div[@class="detail_product_info"]',
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_paging)
    
    def parse_paging(self, response):
        category_num = re.findall('\d+$', response.url)[0]
        limit = [i[1] for i in self.category_nums if i[0] == category_num][0]
        for i in range(limit):
            yield scrapy.Request(response.url + '?page={}'.format(i), callback=self.parse_list)
    
    def parse_list(self, response):
        product_links = response.xpath('//a[@href[contains(., "detail")]]/@href').extract()
        for url in product_links:
            yield scrapy.Request('http://' + self.allowed_domains[0] + url, callback=self.parse_item)
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
            """
        loader = MusinsaLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        
        product_no_obj = re.findall('\d+', response.url)
        if product_no_obj:
            loader.add_value('productNo', product_no_obj[0])
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        
        if response.xpath('//select[@id="option2"]'):
            url = "http://store.musinsa.com/app/svc/production_option"
            data = {'goods_no': product_no_obj[0], 'goods_sub': product_no_obj[1]}
            res = requests.post(url=url, data=data)
            size_labels = [obj['val'] for obj in res.json()]
        else:
            size_labels = response.xpath('//select[@id="option1"]/option/@value').extract()
        
        loader.add_value('originalSizeLabel', size_labels)
        
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
