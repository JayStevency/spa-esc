from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from Crawler.util.handle_string import HandleString


class UniqloLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_digit_from_product_no)
    
    originalSizeLabel_out = str
    color_out = str
