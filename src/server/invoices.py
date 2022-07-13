# standard
import json
import random
# internal
from src.server import req
from src.server.base import Factory


class InvoiceWebFactory(Factory):
    """Invoice Web Factory"""

    def _recieve(self, url):
        res, data = req.get(f'{url}/api/invoice_logs', headers=self.headers)
        return res, json.loads(data.text)

    def _post(self, url, params):
        res = req.post(f'{url}/api/invoices', json=params, headers=self.headers)
        return res

    def get_driver(self):
        drivers = self.cursor.execute("""
            SELECT ID FROM AshkhasList WHERE Peyk = 1
        """)
        return random.choice(drivers.fetchall())[0]

    def get_visitor(self):
        visitors = self.cursor.execute("""
            SELECT ID FROM AshkhasList WHERE visitor = 1
        """)
        return random.choice(visitors.fetchall())[0]

    def get_person(self):
        customers = self.cursor.execute("""
            SELECT ID FROM AshkhasList WHERE Peyk = 0 AND visitor = 0
        """)
        return random.choice(customers.fetchall())[0]

    def get_items(self):
        invoice_item = InvoiceItemWebFactory(self.conn, self.url, self.headers)
        return invoice_item.create()

    def create(self):
        params_dict = {
            'type': random.choice([0, 2]),
            'info': self.fake.text(),
            'total': random.randint(10000, 10000000),
            'items_total': random.randint(10000, 10000000),
            'remain': random.randint(10000, 10000000),
            'tax': random.randint(10000, 1000000),
            'tax_percent': random.randint(1, 10),
            'visitor_price': random.randint(100, 1000),
            'visitor_percent': random.randint(1, 50),
            'discount': random.randint(200, 5000),
            'discount_percent': random.randint(1, 50),
            'items_discount': random.randint(1000, 500000),
            'address': self.fake.address(),
            'person': self.get_person(),
            'visitor': self.get_visitor(),
            'driver': self.get_driver(),
            'items': [self.get_items() for _ in range(random.randint(2, 10))]
        }
        self._post(self.url, params_dict)


class InvoiceItemWebFactory(Factory):
    """Invoice Item Web Factory"""
    @staticmethod
    def _recieve(url):
        res, data = req.get(f'{url}', headers=self.headers)
        return res, json.loads(data.text)

    def get_repo(self):
        repositories = self.cursor.execute("""SELECT Code FROM Negahdari""")
        return random.choice(repositories.fetchall())[0]

    def get_pricelevel(self):
        price_levels = self.cursor.execute("""SELECT ID FROM PriceLevel""")
        return random.choice(price_levels.fetchall())[0]

    def get_product(self):
        products = self.cursor.execute("""SELECT ID FROM KalaList""")
        return random.choice(products.fetchall())[0]

    def create(self):
        params_dict = {
            "price": random.randint(1000, 100000),
            "quantity": random.randint(1, 30),
            "quantity1": 0,
            "quantity2": random.randint(1, 30),
            "unit2_in_unit1": 0,
            "visitor_price": random.randint(100, 1000),
            "visitor_percent": random.randint(1, 50),
            "discount": random.randint(200, 2000),
            "discount_percent": random.randint(1, 50),
            "discount_per_item": random.randint(10, 1000),
            "tax": random.randint(100, 1000),
            "total": random.randint(10000, 1000000),
            "value": random.randint(10000, 1000000),
            "info": self.fake.text(),
            "price_level": self.get_pricelevel(),
            "product": self.get_product(),
            "repository": self.get_repo()
        }
        return params_dict
