# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import CrawlSpider

class UniqloSpider(scrapy.Spider):
    name = 'Uniqlo'
    start_url = 'http://www.uniqlo.kr/search/searchUniqlo.lecs?pageIndex={0}&query=uniqlo'
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(0), callback=self.parse_init)
    
    def parse_init(self, response):
        last_index = response.xpath('//*[@id="endPage"]/a/@href').extract_first()
        last_index = re.search('\d+', last_index)
        
        if last_index is None:
            pass
        else:
            last_index = int(last_index.group()) + 1
        
        for i in range(0, last_index):
            yield scrapy.Request(url=self.start_url.format(i), callback=self.parse_list)
    
    def parse_list(self, response):
        links = response.xpath('//div[@id="BP"]/ul/li/div/div/a/@href').extract()
        
        for link in links:
            product_no = re.search('\d+', link).group()
            yield scrapy.Request(url='http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ' + product_no,
                                 callback=self.parse)
    
    def parse(self, response):
        title = response.xpath('//h2[@id="goodsNmArea"]//text()').extract_first()
        product_no = response.xpath('//li[@class="number"]//text()').extract_first()
        img = response.xpath('//*[@id="prodImgDefault"]/a/img/@src').extract_first()
        price = response.xpath('//*[@id="salePrice"]//text()').extract_first()
        # //*[@id="listChipSize"]/li[2]/a/em
        size_label = response.xpath('//*[@id="listChipSize"]/li/a/@href').extract()
        color = response.xpath('//*[@id="listChipColor"]/li/a/img/@src').extract()
        print(img)
        # yield {
        #     'link': response.url
        # }
        if title is not None and product_no is not None:
            title = title.replace('\n', '')
            title = title.replace('\t', '')
            title = title.replace('\r', '')
            product_no = product_no.replace('상품번호 : ', '')
            yield {
                'title': title,
                'product_no': product_no,
                'img': img,
                'price': price,
                'size_label': size_label,
                'color': color
            }
