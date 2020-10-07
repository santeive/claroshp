from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from datetime import datetime

Base = declarative_base()

class Claro(Base):
    __tablename__ = "claro"

    id = Column(Integer, primary_key=True)
    sku = Column(String, nullable=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    seller = Column(String, nullable=True)
    description = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    url = Column(String, nullable=True)

    price_products = relationship("ClaroProductPrice", back_populates="claro")

    __table_args__ = (UniqueConstraint("sku", name="_sku_unique"),)

class ClaroProductPrice(Base):
    __tablename__ = "claropriceproducts"

    id = Column(Integer, primary_key=True)
    product_id = Column(None, ForeignKey("claro.id"), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    discount=Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    percentage = Column(Integer, default=0, nullable=False)
    date = Column(String, nullable=False)

    claro = relationship("Claro", back_populates="price_products")
