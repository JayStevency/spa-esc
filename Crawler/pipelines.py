# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from Crawler.model.models import Product, db_connect, create_deals_table


class CrawlerPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.productNo_set = set()
    
    def process_item(self, item, spider):
        session = self.Session()
        if item['thumbnail'] is not None and item['productNo'] in self.productNo_set:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.productNo_set.add(item['productNo'])
            product = Product(**item)
            
            try:
                session.add(product)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        
        return item
    
    def close_spider(self, spider):
        pass
