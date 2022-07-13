# fake
from faker import Faker


class Factory(object):
    """Factory"""
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.fake = Faker()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def create_more(self, n):
        for _ in range(0, n):
            self.create()

    def delete_more(self, n):
        for _ in range(0, n):
            self.delete()

    def update_more(self, n):
        for _ in range(0, n):
            self.update()
