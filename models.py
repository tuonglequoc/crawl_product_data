from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, Boolean, BigInteger, Text

BaseModel = declarative_base()


class Product(BaseModel):
    __tablename__ = "product"

    barcode = Column(BigInteger, primary_key=True)
    product_name = Column(Text)
    category = Column(Text)
    country_of_origin = Column(Text)
    link = Column(Text)
    thumbnail = Column(Text)
    price = Column(Integer)
    status = Column(Boolean)
    description = Column(Text)
    remarks = Column(Text)
