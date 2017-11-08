# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from Crawler.items import Product


class UniqloSpider(scrapy.Spider):
    name = 'Uniqlo'
    start_url = 'http://www.uniqlo.kr/search/searchUniqlo.lecs?pageIndex={0}&query=uniqlo'
    item_fields = {
        'title': '//h2[@id="goodsNmArea"]//text()',
        'productNo': '//li[@class="number"]//text()',
        'thumbnail': '//*[@id="prodImgDefault"]/a/img/@src',
        'price': '//*[@id="salePrice"]//text()',
        'originalSizeLabel': '//*[@id="listChipSize"]/li/a/em/text()',
        'color': '//*[@id="listChipColor"]/li/a/img/@alt',
        'material': '//*[@id="prodDetail"]/div/dl[2]/dd/text()',
        'category': '//*[@id="prodInfo"]/p/a[2]/text()'
    }
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(0), callback=self.parse_init)
    
    def parse_init(self, response):
        last_index = response.xpath('//*[@id="endPage"]/a/@href').extract_first()
        last_index = re.search('\d+', last_index)
        
        if last_index is None:
            pass
        else:
            last_index = int(last_index.group()) + 1

        self.parse_list(response=response)
        # while True:
        #     yield self.parse_list(response=response)
        #     break
        
        # for i in range(1, last_index):
        for i in range(2):
            yield scrapy.Request(url=self.start_url.format(i), callback=self.parse_list)
    
    def parse_list(self, response):
        links = response.xpath('//div[@id="BP"]/ul/li/div/div/a/@href').extract()
        
        for link in links:
            product_no = re.search('\d+', link).group()
            yield SplashRequest(url='http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ' + product_no,
                                callback=self.parse,
                                args={'wait': 0.5}
                                )
    
    def parse(self, response):
        loader = ItemLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
