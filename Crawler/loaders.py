from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Join
from Crawler.util.handle_string import HandleString, ExtractPrice, AddHttpString, StringToList
from w3lib.html import replace_entities, replace_escape_chars
from Crawler.util.common import TakeUnique, replace_useless_chars


class UniqloLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    salePrice_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_digit_from_product_no)
    
    originalCategory_out = str
    originalSizeLabel_out = str
    color_out = str
    
    detailImages_out = str
    description_out = str


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
    
    detailImages_out = str
    description_out = str


class BalaanLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = MapCompose(HandleString.extract_digit_from_price)
    title_in = MapCompose(replace_entities, replace_escape_chars)
    brand_in = MapCompose(replace_entities, replace_escape_chars)
    originalCategory_in = TakeUnique()
    originalSizeLabel_in = TakeUnique()
    
    originalCategory_out = str
    category_out = str
    thumbnail_out = str
    originalSizeLabel_out = str


class ZaraLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = ExtractPrice()
    thumbnail_in = AddHttpString()
    detailImages_in = AddHttpString()
    
    originalSizeLabel_out = str
    
    detailImages_out = str
    description_out = str


class SpaoLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    originalSizeLabel_in = StringToList()
    color_in = StringToList()
    price_in = ExtractPrice()
    salePrice_in = ExtractPrice()
    
    originalCategory_out = str
    originalSizeLabel_out = str
    color_out = str
    
    detailImages_out = str
    description_out = str


class MusinsaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    thumbnail_in = AddHttpString()
    price_in = ExtractPrice()
    salePrice_in = ExtractPrice()
    originalSizeLabel_in = TakeUnique()
    
    detailImages_in = AddHttpString()
    
    originalSizeLabel_out = str
    
    detailImages_out = str
    description_out = str
    detailHtml_out = str


class HnmLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    thumbnail_in = AddHttpString()
    price_in = ExtractPrice()
    salePrice_in = ExtractPrice()
    
    detailImages_in = AddHttpString()
    
    originalSizeLabel_out = str
    
    detailImages_out = str
    description_out = str


class HipHoperLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = ExtractPrice()
    originalSizeLabel_in = TakeUnique()
    
    originalSizeLabel_out = str
    
    detailImages_out = str
    description_out = str
    detailHtml_out = str


class SSFShopLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    originalCategory_in = MapCompose(replace_useless_chars)
    originalSizeLabel_out = str
    
    originalCategory_out = str
    detailImages_out = str
    description_out = str
    detailHtml_out = str


class A29CMLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(replace_useless_chars)
    price_in = Compose(TakeFirst(), ExtractPrice())
    salePrice_in = Compose(TakeFirst(), ExtractPrice())
    thumbnail_in = AddHttpString()
    detailImages_in = AddHttpString()
    description_in = MapCompose(replace_useless_chars)
    
    originalSizeLabel_out = str
    
    originalCategory_out = str
    detailImages_out = str
    description_out = str
    detailHtml_out = str


class MujiLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = Compose(Join(''))
    salePrice_in = Compose(Join(''))
    
    title_out = Compose(Join(''))
    originalSizeLabel_out = str

    originalCategory_out = str
    detailImages_out = str
    description_out = str
    detailHtml_out = str
