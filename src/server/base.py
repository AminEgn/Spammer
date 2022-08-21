# fake
from faker import Faker


class Factory(object):
    """Factory"""
    def __init__(self, conn=None, url=None, headers=None):
        self.conn = conn
        self.headers = headers
        self.url = url
        self.fake = Faker()

    @property
    def cursor(self):
        return self.conn.cursor()

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
