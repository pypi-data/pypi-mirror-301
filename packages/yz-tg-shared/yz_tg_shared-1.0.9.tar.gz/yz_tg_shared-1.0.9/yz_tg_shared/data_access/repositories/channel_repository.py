from yz_tg_shared.entities.channel import Channel
from yz_tg_shared.models.channel_model import ChannelUpdateModel


class ChannelRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Channel).all()

    def UpdateOffset(self, channel_id: int, channel_offset_message_id: int):
        self.session.query(Channel).filter(Channel.ChannelID == channel_id).update({Channel.OffsetMessageID: channel_offset_message_id},
                                                                                   synchronize_session=False)
        self.session.commit()
        # channel = self.session.query(Channel).filter_by(ChannelID=channel_id).first()
        # if channel:
        #     channel.OffsetMessageID = channel_offset_message_id
        #     self.session.commit()
        #     self.session.refresh(channel)
        # return channel
