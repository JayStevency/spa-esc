# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.loaders import BalaanLoader
from Crawler.items import Product


class BalaanSpider(CrawlSpider):
    name = 'balaan'
    allowed_domains = ['balaan.co.kr']
    allow_categories = [
        '002002012', '002002009', '002002007', '002002006', '002002008', '002002002',
        '002002003', '002002004', '002002005', '002002013', '002002010', '001002014',
        '002002013', '002002010', '002002003', '002002008', '002002009', '002002001',
        '002002002', '002002006', '002002007', '002002004', '002002012', '002002015',
    ]
    start_urls = ('http://www.balaan.co.kr/shop/goods/goods_list.php?category={}'.format(no) for no in allow_categories)
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }
    
    rules = (
        Rule(LinkExtractor(allow=('page=',), deny=('002002001', '002002$', '001002005', '001002$'))),
        Rule(LinkExtractor(allow=('goodsno=\d+',)), callback='parse_item'),
    )
    
    def parse_item(self, response):
        loader = BalaanLoader(item=Product(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('shopHost', 'balaan')
        loader.add_xpath('title', '//p[@class="detail-info__spec--description"]/text()')
        loader.add_xpath('productNo', '//dd[@class="detail-spec__item-value"]//strong/text()')
        loader.add_xpath('price', '//span[@id="price"]/text()')
        loader.add_xpath('brand', '//header[@class="detail-info__spec-header"]//a[contains(@href, "brand")]/text()')
        loader.add_xpath('originalCategory', '//div[@class="detail-info__spec--category"]//a/text()')
        loader.add_xpath('thumbnail', '//ul[@class="detail-info__thembnail-list"]//img/@src')
        loader.add_xpath('originalSizeLabel', '//li[@class="detail-spec__option-item"]//option/@value')
        
        return loader.load_item()
