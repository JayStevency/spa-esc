# -*- coding: utf-8 -*-
import scrapy
import re
from Crawler.items import Product
from Crawler.loaders import SSFShopLoader


class SsfshopSpider(scrapy.Spider):
    name = 'ssfshop'
    allowed_domains = ['ssfshop.com']
    start_urls = ['http://www.ssfshop.com/WOMEN/list?dspCtgryNo=SFMA41&brandShopNo=',
                  'http://www.ssfshop.com/MEN/list?dspCtgryNo=SFMA42&brandShopNo=']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    
    item_fields = {
        'title': '//meta[@property="rb:itemName"]/@content',
        'productNo': '//meta[@property="rb:itemId"]/@content',
        'thumbnail': '//*[@class="side01"]//img/@src',
        'price': '//meta[@property="rb:originalPrice"]/@content',
        'salePrice': '//meta[@property="rb:salePrice"]/@content',
        'originalSizeLabel': '//input[@name="sizeItmNm"]/@value',
        'originalCategory': '//span[@class="bracket"]/a/text()',
        'color': '//input[@id="colorNm"]/@value',
        'detailImages': '//div[@class="prd-img"]//img/@src',
        'description': '//meta[@property="og:description"]//@context',
        'detailHtml': '//div[@id="detailInfo"]',
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_paging)
    
    def parse_paging(self, response):
        limit = int(response.xpath("//a[@class[contains(., 'last')]]/@id").extract_first())
        for i in range(1, limit):
            yield scrapy.Request(response.url + '&currentPage={}'.format(i), callback=self.parse_list)
    
    def parse_list(self, response):
        product_links = response.xpath('//a[@href[contains(., "good")]]/@href').extract()
        for url in product_links:
            yield scrapy.Request('http://www.' + self.allowed_domains[0] + url, callback=self.parse_item)
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
            """
        loader = SSFShopLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        split_url = re.sub('http://www.ssfshop.com/', '', response.url).split('/')
        brand = split_url[0]
        loader.add_value('brand', brand)
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
