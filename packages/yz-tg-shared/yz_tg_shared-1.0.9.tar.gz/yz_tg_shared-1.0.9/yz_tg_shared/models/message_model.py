from pydantic import BaseModel
from typing import Optional


class MessageModel(BaseModel):
    MessageID: int
    MsgID: int
    ChannelID: int
    MessageDate: str
    MessageText: str
    IsModified: Optional[bool]

    class Config:
        orm_mode = True


class MessageCreateModel(BaseModel):
    ChannelID: int
    MsgID: int
    MessageDate: str
    MessageText: str
    IsModified: Optional[bool] = False


class MessageUpdateModel(BaseModel):
    MessageID: int
    MsgID: int
    MessageText: str
    IsModified: Optional[bool] = True
