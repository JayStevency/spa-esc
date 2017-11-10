# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from Crawler.loders.item_loader import UniqloLoader
from Crawler.items import Product


class UniqloSpider(CrawlSpider):
    name = 'uniqlo'
    allowed_domains = ['www.uniqlo.kr']
    start_urls = [
        'http://www.uniqlo.kr/display/displayShop.lecs?storeNo=22&siteNo=9&displayNo=UQ1A01A07'
        '&displayMallNo=UQ1&tracking=header_logo&stonType=P']
    
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
    
    rules = (
        Rule(LinkExtractor(allow=('displayNo=UQ*',)), callback='parse_dummy', follow=True),
    )
    
    def parse_dummy(self, response):
        if 'goodsNo=UQ' in response.url:
            yield SplashRequest(response.url, callback=self.parse_item, args={'wait': 5})
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
            """
        loader = UniqloLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()