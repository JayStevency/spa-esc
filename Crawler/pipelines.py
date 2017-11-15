# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from Crawler.model.models import Product, db_connect, create_deals_table
from Crawler.util.common import check_essential_element


class FilterPipeline(object):
    def __init__(self):
        self.item_set = set()
    
    def process_item(self, item, spider):
        check_item = (item.get('brand'), item.get('productNo'))
        if check_item in self.item_set:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.item_set.add(check_item)
        return item


class CrawlerPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        session = self.Session()
        if check_essential_element(item):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            product = Product(**item)
            
            try:
                exist_product = session.query(Product).filter_by(productNo=item.get('productNo'),
                                                                 brand=item.get('brand'))
                if exist_product.first() is None:
                    session.add(product)
                else:
                    exist_product.update(item)
            except:
                session.rollback()
                raise
            finally:
                session.commit()
                session.close()
        
        return item
    
    def close_spider(self, spider):
        pass
