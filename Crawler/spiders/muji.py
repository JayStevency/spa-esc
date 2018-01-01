# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.items import Product
from Crawler.loaders import MujiLoader


class MujiSpider(CrawlSpider):
    name = 'muji'
    allowed_domains = ['www.mujikorea.net']
    start_urls = [
        'http://www.mujikorea.net/display/displayShop.lecs?storeNo=1&siteNo=13013&displayNo=MJ1A84&displayMallNo=MJ1']
    
    allowed_category_links = (r'displayPromotion', r'displayPlan', r'displayShop',)
    
    rules = (
        Rule(LinkExtractor(allow=allowed_category_links), follow=True),
        Rule(LinkExtractor(allow=r'goodsNo='), callback='parse_item'),
    )
    
    item_fields = {
        'title': '//div[@class="onenone_infoArea"]/dl/dt[position()=1]/text()',
        'productNo': '//form[@name="submitForm"]/input[@name="goodsNo"]/@value',
        'thumbnail': '//img[@class="image_holder"]/@src',
        'price': '//dt[text()[contains(.,"판매가")]]/following-sibling::dd//text()',
        'salePrice': '//dt[text()[contains(.,"인하가") or contains(.,"세일가")]]/following-sibling::dd/strong/text()',
        'originalSizeLabel': '//dd[@class="size_c"]//img/@alt',
        'color': '//dd[@class="color_c"]//img/@alt',
        'originalCategory': '//div[@class="map_con"]//text()',
        'detailImages': '//ul[@class="small_image_list"]//a/@href',
        'description': '//div[@class="user_con mgb30"]/text()',
        'detailHtml': '//div[@class="user_con mgb30"]'
    }
    
    fields_regex = {
        'title': '\S+',
        'productNo': '',
        'thumbnail': '',
        'price': '\d',
        'salePrice': '\d',
        'originalSizeLabel': '',
        'color': '',
        'originalCategory': '\S+',
        'detailImages': '',
        'description': '\S+',
        'detailHtml': ''
    }
    
    def parse_item(self, response):
        loader = MujiLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath, re=self.fields_regex[field])
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        
        return loader.load_item()
    
    def closed(self, reason):
        self.logger.info(reason)
