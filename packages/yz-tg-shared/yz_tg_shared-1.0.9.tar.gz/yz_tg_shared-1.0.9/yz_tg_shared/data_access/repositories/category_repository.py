from yz_tg_shared.entities.category import Category


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Category).all()
