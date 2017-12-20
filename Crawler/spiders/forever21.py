# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.loaders import Forever21Loader
from Crawler.items import Product


class Forever21Spider(CrawlSpider):
    name = 'forever21'
    allowed_domains = ['www.forever21.co.kr']
    start_urls = ['http://www.forever21.co.kr/']
    
    item_fields = {
        'title': '//h1[@class="item_name_p"]/text()',
        'productNo': '/html/head/meta[@property="og:url"]/@content',
        'thumbnail': '//*[@id="ctl00_MainContent_productImage"]/@src',
        'price': '//*[@id="spanProductPrice"]/text() | //*[@id="spanProductPrice"]/span[1]/text()',
        'salePrice': '//*[@id="spanProductPrice"]/span[2]/text()',
        'originalSizeLabel': '//*[@id="ulProductSize"]/li/label/text()',
        'color': '//*[@id="spanSelectedColorName"]/text()',
        'material': '//*[text()[contains(., "FABRIC")]]/text()',
        'originalCategory': '//*[@id="div_breadcrumb"]/a/u/text()',
        'detailImages': '//ul[@id="pdp_thumbnail"]/li/a/img/@src',
        'description': '//*[@class="itemdetailcontent"]/*/text()'
    }
    
    denied_category = ('br=acc', 'br=shoesnbag', 'br=f21_acc', 'br=f21_shoesnbag',
                       'category=f21_acc_beauty_makeup_facetool')
    denied_etc = ('Login.aspx',)
    rules = (
        Rule(LinkExtractor(allow=('productid', 'ProductID')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('category',),
                           deny=denied_category + denied_etc),
             follow=True),
    )
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.forever21.co.kr/Product/Product.aspx?BR=f21&Category=f21_app_knitncardigan&ProductID=2000225035&VariantID=
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
            """
        loader = Forever21Loader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
