# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.loders.item_loader import Forever21Loader
from Crawler.items import Product


class Forever21Spider(CrawlSpider):
    name = 'forever21'
    allowed_domains = ['www.forever21.co.kr']
    start_urls = ['http://www.forever21.co.kr/']
    
    item_fields = {
        'title': '//h1[@class="item_name_p"]/text()',
        'productNo': '/html/head/meta[@property="og:url"]/@content',
        'thumbnail': '//*[@id="ctl00_MainContent_productImage"]/@src',
        'price': '//*[@id="spanProductPrice"]/text()',
        'originalSizeLabel': '//*[@id="ulProductSize"]/li/label/text()',
        'color': '//*[@id="spanSelectedColorName"]/text()',
        'material': '//*[@id="aspnetForm"]/div[3]/div[4]/div/section/div/article/div/div[1]/p/text()',
        'category': '//*[@id="div_breadcrumb"]/a[3]/u/text()'
    }
    
    rules = (
        Rule(LinkExtractor(allow=('productid', 'ProductID')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('category',), deny=('br=acc', 'br=shoesnbag', 'br=f21_acc', 'br=f21_shoesnbag')),
             follow=True),
    )
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
            """
        loader = Forever21Loader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
