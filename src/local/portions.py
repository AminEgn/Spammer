# standard
import random
# internal
from src.local.base import Factory


class PortionFactory(Factory):
    """Portion Factory"""

    def get_visitor(self):
        visitors = self.cursor.execute("""
            SELECT ID FROM AshkhasList WHERE visitor = 1
        """)
        return random.choice(visitors.fetchall())[0]

    def get_product(self):
        products = self.cursor.execute("""SELECT ID FROM KalaList""")
        return random.choice(products.fetchall())[0]

    def create(self):
        params = [self.get_visitor(), self.get_product(), random.randint(1, 15)]
        self.cursor.execute("""
            INSERT INTO ASHKHASVISITOR(IDShakhs, IDKala, Perc) VALUES(?, ?, ?)
        """, params)
        self.cursor.commit()
