from datetime import datetime

from pydantic.fields import Optional, List

from yz_tg_shared.entities.message import Message
from yz_tg_shared.models.message_model import MessageCreateModel, MessageUpdateModel


class MessageRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Message).all()

    def create(self, message_data: MessageCreateModel):
        new_message = Message(
            ChannelID=message_data.ChannelID,
            MessageDate=message_data.MessageDate,
            MsgID=message_data.MsgID,
            MessageText=message_data.MessageText,
            IsModified=message_data.IsModified
        )
        self.session.add(new_message)
        self.session.commit()
        self.session.refresh(new_message)
        return new_message

    def update(self, message_data: MessageUpdateModel):
        message = self.session.query(Message).filter_by(MessageID=message_data.MessageID).first()
        if message:
            message.MessageText = message_data.MessageText
            message.MsgID = message_data.MsgID
            message.IsModified = message_data.IsModified
            self.session.commit()
            self.session.refresh(message)
        return message

    def update_is_hidden(self, message_data: MessageUpdateModel):
        message = self.session.query(Message).filter_by(MessageID=message_data.MessageID).first()
        if message:
            message.IsModified = message_data.IsModified
            self.session.commit()
            self.session.refresh(message)
        return message

    def get_filtered(self, group_id: Optional[int] = None, date_from: Optional[datetime] = None,
                     date_to: Optional[datetime] = None, is_modified: Optional[bool] = None) -> List[Message]:
        query = self.session.query(Message)

        if group_id is not None:
            query = query.filter(Message.GroupID == group_id)

        if date_from is not None:
            query = query.filter(Message.MessageDate >= date_from)

        if date_to is not None:
            query = query.filter(Message.MessageDate <= date_to)

        if is_modified is not None:
            query = query.filter(Message.IsModified == is_modified)

        return query.all()
