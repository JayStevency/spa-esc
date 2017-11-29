# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Crawler.items import Product
from Crawler.loaders import SpaoLoader


def process_ctg_value(value):
    m = re.search('disp_ctg_no\:\'\d+\'', value)
    if m:
        ctg_reg_obj = re.search('\d+', m.group())
        ctg_no = ctg_reg_obj.group()
        return 'http://spao.elandmall.com/dispctg/initDispCtg.action?disp_ctg_no=%s' % ctg_no


def process_detail_value(value):
    m = re.search('goods_no\:\'\d+\'', value)
    if m:
        good_reg_obj = re.search('\d+', m.group())
        good_no = good_reg_obj.group()
        return 'http://spao.elandmall.com/goods/initGoodsDetail.action?goods_no=%s' % good_no


class SpaoSpider(CrawlSpider):
    name = 'spao'
    allowed_domains = ['spao.elandmall.com']
    start_urls = ['http://spao.elandmall.com/main/initMain.action']
    
    item_fields = {
        'title': '//strong[@class="goods_name"]/text()',
        'productNo': '//*[@id="detail_goods_no"]/@value',
        'thumbnail': '//img[@class="dt_ve_ct_img"]/@src',
        'price': '//meta[@property="recopick:price"]/@content',
        'salePrice': '//meta[@property="recopick:sale_price"]/@content',
        'originalSizeLabel': '//th[text()[contains(.,"치수")]]/following-sibling::td/text()',
        'color': '//th[text()[contains(.,"색상")]]/following-sibling::td/text()',
        'material': '//th[text()[contains(.,"제품 소재")]]/following-sibling::td/text()',
        'originalCategory': '//*[@selected="selected"]/text()'
    }
    
    rules = (
        Rule(LinkExtractor(allow='dispctg', attrs=('onclick',), process_value=process_ctg_value), follow=True),
        Rule(LinkExtractor(allow=r'goods_no\=\d+', attrs=('onclick',), process_value=process_detail_value),
             callback='parse_item'),
    )
    
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            @url http://www.uniqlo.kr/display/showDisplayCache.lecs?goodsNo=UQ31088277&displayNo=UQ1A02A01A27&stonType=P&storeNo=22&siteNo=9
            @returns items 1 16
            @returns requests 0 0
            @scrapes  url thumbnail brand title price category productNo material originalSizeLabel color
        """
        loader = SpaoLoader(item=Product(), response=response)
        for field, xpath in self.item_fields.items():
            loader.add_xpath(field, xpath)
        loader.add_value('shopHost', self.name.lower())
        loader.add_value('url', response.url)
        loader.add_value('brand', self.name.lower())
        return loader.load_item()
