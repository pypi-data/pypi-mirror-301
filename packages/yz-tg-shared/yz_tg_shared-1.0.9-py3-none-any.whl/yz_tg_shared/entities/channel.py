from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from yz_tg_shared.entities.base import Base
from yz_tg_shared.entities.category import Category


class Channel(Base):
    __tablename__ = 'Channels'
    ChannelID = Column(Integer, primary_key=True, autoincrement=True)
    TelegramGrpID = Column(Integer, nullable=False)
    OffsetMessageID = Column(Integer, nullable=True)
    ChannelName = Column(String(255), nullable=False)
    CategoryID = Column(Integer, ForeignKey('Categories.CategoryID'))
    SignatureLinesCount = Column(Integer, nullable=True)
    category = relationship('Category', back_populates='channels')


Category.channels = relationship('Channel', order_by=Channel.ChannelID, back_populates='category')
