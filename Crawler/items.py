# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field(output_processor=TakeFirst())
    thumbnail = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    # 공백 제거
    title = scrapy.Field(output_processor=TakeFirst())
    # , 원 제거
    price = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    # 상품번호 : 제거
    productNo = scrapy.Field(output_processor=TakeFirst())
    material = scrapy.Field(output_processor=TakeFirst())
    originalSizeLabel = scrapy.Field(output_processor=str)
    color = scrapy.Field(output_processor=str)
