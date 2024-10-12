from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yz_tg_shared.entities.base import Base
from yz_tg_shared.data_access.repositories.category_repository import CategoryRepository
from yz_tg_shared.data_access.repositories.channel_repository import ChannelRepository
from yz_tg_shared.data_access.repositories.message_repository import MessageRepository
from sqlalchemy.exc import OperationalError
import time

class UnitOfWork:
    def __init__(self, db_url, retries=5, delay=0.5):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.retries = retries
        self.delay = delay

    def __enter__(self):
        self.session = self.Session()
        self.categories = CategoryRepository(self.session)
        self.channels = ChannelRepository(self.session)
        self.messages = MessageRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        retry_count = 0
        while retry_count < self.retries:
            try:
                if exc_type:
                    self.session.rollback()
                else:
                    self.session.commit()
                self.session.close()
                break
            except OperationalError as e:
                if "database is locked" in str(e):
                    retry_count += 1
                    time.sleep(self.delay)
                else:
                    raise
        else:
            raise Exception(f"Database is locked after {self.retries} retries")
