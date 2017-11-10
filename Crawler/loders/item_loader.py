from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from Crawler.util.handle_string import HandleString
from Crawler.util.pick_tag import Picker


class UniqloLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_digit_from_product_no)
    
    originalSizeLabel_out = str
    color_out = str


class Forever21Loader(ItemLoader):
    default_output_processor = TakeFirst()
    
    title_in = MapCompose(HandleString.remove_whitespace)
    price_in = MapCompose(HandleString.extract_digit_from_price)
    productNo_in = MapCompose(HandleString.extract_product_id_from_url)
    
    # p태그 리스트중 데이터 픽업 함수 개발
    # material_out = MapCompose(Picker.picker_fabric)
    originalSizeLabel_out = str
    color_out = str
