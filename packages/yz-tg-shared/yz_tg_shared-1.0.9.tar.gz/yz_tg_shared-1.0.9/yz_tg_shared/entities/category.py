from sqlalchemy import Column, Integer, String, Text
from yz_tg_shared.entities.base import Base


class Category(Base):
    __tablename__ = 'Categories'
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(255), nullable=False)
    Description = Column(Text)
