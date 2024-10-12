from sqlalchemy import Column, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from yz_tg_shared.entities.base import Base
from yz_tg_shared.entities.channel import Channel


class Message(Base):
    __tablename__ = 'Messages'
    MessageID = Column(Integer, primary_key=True, autoincrement=True)
    ChannelID = Column(Integer, ForeignKey('Channels.ChannelID'))
    MsgID = Column(Integer, nullable=False)
    MessageDate = Column(DateTime, nullable=False)
    MessageText = Column(Text, nullable=False)
    IsModified = Column(Boolean, default=False)
    channel = relationship('Channel', back_populates='messages')


Channel.messages = relationship('Message', order_by=Message.MessageID, back_populates='channel')
