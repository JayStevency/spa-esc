import scrapy


class Product(scrapy.Item):
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
