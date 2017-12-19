# -*- coding: utf-8 -*-
import scrapy
import os
import re
from scrapy_splash import SplashRequest
from Crawler.items import Product
from Crawler.loaders import SpaoLoader


class SpaoSpider(scrapy.Spider):
    name = 'spao'
    allowed_domains = ['spao.elandmall.com']
    start_urls = ['http://spao.elandmall.com/search/search.action?kwd=*#hashPage%s'
                  '/mall_no=0000037&sort=7&preKwd=&category_1depth=&color_info='
                  '&category_2depth=&deliCostFreeYn=&vend_nm='
                  '&deliCostPoliNo=&applyEndDate=&vend_no='
                  '&dispStartDate=&newGoodsStartDate='
                  '&min_price=&category_4depth=&brand_nm='
                  '&srchFd=null&setDicountYn=&category_3depth=&applyStartDate='
                  '&_=1512003966634&min_rate=&brand_no=&category_5depth=null'
                  '&category_6depth=null&kwd=&listType=image&pageSize=60&giftYn='
                  '&newGoodsEndDate=&max_rate=&reSrch=&size_info='
                  '&oneMoreYn=&welfareYn=&staffDCYn=&dispEndDate='
                  '&discountYn=&max_price=&material_info=&preFlag=' % i for i in range(50)]
    
    item_fields = {
        'title': '//strong[@class="goods_name"]/text()',
        'productNo': '//*[@id="detail_goods_no"]/@value',
        'thumbnail': '//img[@class="dt_ve_ct_img"]/@src',
        'price': '//meta[@property="recopick:price"]/@content',
        'salePrice': '//meta[@property="recopick:sale_price"]/@content',
        'originalSizeLabel': '//th[text()[contains(.,"치수")]]/following-sibling::td/text()',
        'color': '//th[text()[contains(.,"색상")]]/following-sibling::td/text()',
        'material': '//th[text()[contains(.,"제품 소재")]]/following-sibling::td/text()',
        'originalCategory': '//*[@selected="selected"]/text()',
        'detailImages': '//*[@class="detail_html"]//img/@src',
    }
    
    custom_settings = {
        'SPLASH_URL': os.environ['SPLASH_URL'],
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse_list, args={'wait': 5})
    
    def parse_list(self, response):
        goods_no_list = response.xpath('//a/@onclick').re(r'goods_no\:\'\d+')
        for good_reg_obj in goods_no_list:
            good_no = ''.join(re.findall('\d', good_reg_obj))
            yield scrapy.Request('http://spao.elandmall.com/goods/initGoodsDetail.action?goods_no=%s' % good_no,
                                 callback=self.parse_item)
    
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
