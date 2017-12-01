# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.items import Product
from Crawler.loaders import MusinsaLoader


class MusinsaSpider(CrawlSpider):
    name = 'musinsa'
    allowed_domains = ['store.musinsa.com']
    start_urls = ['http://store.musinsa.com/app/']
    
    item_fields = {
        'title': '//span[@class="product_title"]/span[not(@class)]/text()',
        'thumbnail': '//*[@class="product-img"]/img/@src',
        'price': '//span[@id="goods_price"]/*/text() | //span[@id="goods_price"]/text()',
        'salePrice': '//span[@id="sale_price"]/text()',
        'material': '//li[text()[contains(.,"소재")]]/following-sibling::li/text()',
        'originalCategory': '//*[@class="item_categories"]/a/text()',
        'brand': '//*[@class="brand"]/a/span/text()'
    }
    
    rules = (
        Rule(LinkExtractor(allow=r'lists/'), follow=True),
        Rule(LinkExtractor(allow=r'detail/'), callback='parse_item', follow=True),
    )
    
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
        
        size_labels = response.xpath('//tr[@class="order_size_save"]/following-sibling::tr/th/text()').extract()
        if not size_labels:
            size_labels = response.xpath('//select[@id="option1"]/option/@value').extract()
        
        loader.add_value('originalSizeLabel', size_labels)
        product_no_obj = re.findall('\d+', response.url)
        if product_no_obj:
            loader.add_value('productNo', product_no_obj[0])
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        
        return loader.load_item()
