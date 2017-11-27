from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from Crawler.util.handle_string import HandleString
from w3lib.html import replace_entities, replace_escape_chars


class UniqloLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    salePrice_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_digit_from_product_no)
    
    originalCategory_out = str
    originalSizeLabel_out = str
    color_out = str


class Forever21Loader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    salePrice_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_product_id_from_url)
    material_in = MapCompose(HandleString.remove_whitespace)
    
    originalCategory_out = str
    originalSizeLabel_out = str
    color_out = str


class BalaanLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(replace_entities, replace_escape_chars)
    brand_in = MapCompose(replace_entities, replace_escape_chars)
    
    category_out = Identity()
    thumbnail_out = Identity()
    originalSizeLabel_out = Identity()
