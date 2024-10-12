from pydantic import BaseModel


class ChannelModel(BaseModel):
    ChannelID: int
    TelegramGrpID: int
    OffsetMessageID: int
    ChannelName: str
    SignatureLinesCount: int
    CategoryID: int

    class Config:
        orm_mode = True


class ChannelUpdateModel(BaseModel):
    ChannelID: int
    OffsetMessageID: int
    SignatureLinesCount: int
    CategoryID: str
