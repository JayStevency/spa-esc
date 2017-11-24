# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    salePrice = scrapy.Field()
    category = scrapy.Field()
    originalCategory = scrapy.Field()
    productNo = scrapy.Field()
    material = scrapy.Field()
    originalSizeLabel = scrapy.Field()
    color = scrapy.Field()
    
