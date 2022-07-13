# standard
import random
import sqlite3
from datetime import datetime
# internal
from src.local.base import Factory


API_DB_PATH = r'F:\Projects\Pythonic\PROTOMAPI\MAPI\db.sqlite3'
conn = sqlite3.connect(API_DB_PATH)


class InvoiceFactory(Factory):
    """Invoice Factory"""
    def get_driver(self):
        drivers = self.cursor.execute("""
            SELECT mid FROM core_person WHERE courier = 1
        """)
        return random.choice(drivers.fetchall())[0]

    def get_visitor(self):
        visitors = self.cursor.execute("""
            SELECT mid FROM core_person WHERE visitor = 1
        """)
        return random.choice((visitors.fetchall()))[0]

    def get_customer(self):
        customers = self.cursor.execute("""
            SELECT mid FROM core_person WHERE courier = 0 AND visitor = 0
        """)
        return random.choice(customers.fetchall())[0]

    def set_items(self, invoice_id):
        invoice_item = InvoiceItemFactory(self.conn)
        invoice_item.create(invoice_id)

    def create(self):
        params = [
            random.choice([0, 2]),
            self.fake.text(),
            random.randint(10000, 10000000),
            random.randint(10000, 10000000),
            random.randint(10000, 10000000),
            random.randint(10000, 1000000),
            random.randint(1, 10),
            random.randint(100, 1000),
            random.randint(1, 50),
            random.randint(200, 5000),
            random.randint(1, 50),
            random.randint(1000, 500000),
            self.get_customer(),
            self.get_driver(),
            self.get_visitor(),
            datetime.now().isoformat(),
            datetime.now().isoformat(),
        ]
        self.cursor.execute("""
            INSERT INTO core_invoice(
                type, info, total, items_total, remain, tax, tax_percent, visitor_price,
                visitor_percent, discount, discount_percent, items_discount, person_id,
                driver_id, visitor_id, created_at, updated_at
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, params)
        invoice_id = self.cursor.lastrowid
        self.conn.commit()
        for _ in range(random.randint(1, 7)):
            self.set_items(invoice_id)


class InvoiceItemFactory(Factory):
    """Invoice Item Factory"""
    def get_repository(self):
        repositories = self.cursor.execute("""SELECT mid FROM core_repository""")
        return random.choice(repositories.fetchall())[0]

    def get_pricelevel(self):
        price_levels = self.cursor.execute("""SELECT mid FROM core_pricelevel""")
        return random.choice(price_levels.fetchall())[0]

    def get_product(self):
        products = self.cursor.execute("""SELECT mid FROM core_product""")
        return random.choice(products.fetchall())[0]

    def create(self, invoice_id):
        params = [
            random.randint(1000, 100000),
            random.randint(1, 30),
            0,
            random.randint(1, 30),
            0,
            random.randint(100, 1000),
            random.randint(1, 50),
            random.randint(200, 2000),
            random.randint(1, 50),
            random.randint(10, 1000),
            random.randint(100, 1000),
            random.randint(10000, 1000000),
            random.randint(10000, 1000000),
            self.fake.text(),
            invoice_id,
            self.get_pricelevel(),
            self.get_product(),
            self.get_repository(),
        ]
        self.cursor.execute("""
            INSERT INTO core_invoiceitem(
                price, quantity, quantity1, quantity2, unit2_in_unit1, visitor_price,
                visitor_percent, discount, discount_percent, discount_per_item, tax,
                total, value, info, invoice_id, price_level_id, product_id, repository_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, params)
        self.conn.commit()


if __name__ == '__main__':
    inf = InvoiceFactory(conn)
    inf.create()
