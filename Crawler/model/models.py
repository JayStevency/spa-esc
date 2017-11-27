import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from Crawler.model import settings

DeclarativeBase = declarative_base()


class Product(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    url = Column('url', String(500), nullable=True)
    thumbnail = Column('thumbnail', String(500), nullable=True)
    brand = Column('brand', String(255), nullable=True)
    shopHost = Column('shopHost', String(255), nullable=True)
    title = Column('title', String(255), nullable=True)
    price = Column('price', Integer, nullable=True, default=0)
    salePrice = Column('salePrice', Integer, nullable=True, default=0)
    category = Column('category', String(255), nullable=True)
    productNo = Column('productNo', String(255), nullable=True)
    material = Column('material', String(500), nullable=True)
    originalCategory = Column('originalCategory', String(500), nullable=True)
    originalSizeLabel = Column('originalSizeLabel', String(500), nullable=True)
    color = Column('color', String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())


def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE, query={'charset': 'utf8'}), encoding='utf8')
