# standard
import random
# internal
from src.local.base import Factory


class RepositoryFactory(Factory):
    """Repository Factory"""
    def create(self):
        name = f'Store_{self.fake.name()}'
        self.cursor.execute("""INSERT INTO Negahdari(Name) VALUES (?)""", [name])
        self.cursor.commit()


class CategoryFactory(Factory):
    """Category Factory"""
    def create(self):
        parent = 0
        has_parent = random.choices([True, False], [1, 8])
        if has_parent[0]:
            parents = self.cursor.execute("""SELECT * FROM GroupKala""")
            parentfetch = parents.fetchall()
            if parentfetch:
                parent = random.choice(parentfetch)[0]

            name = f"Category_{self.fake.company()}"
            self.cursor.execute("""
            INSERT INTO GroupKala(ParentID, GroupKala) 
            VALUES (?, ?)   
            """, [parent, name])
            self.cursor.commit()


class ProductFactory(Factory):
    """Product Factory"""
    def get_category(self):
        rc = random.choices([True, False], [1, 40])
        if rc[0]:
            c = CategoryFactory(self.conn)
            c.create()

        category = self.cursor.execute("""SELECT * FROM GroupKala""")
        categoryfetch = category.fetchall()
        if not categoryfetch:
            c = CategoryFactory(self.conn)
            c.create()
        get = random.choice(categoryfetch)[0]
        return get

    def set_prices(self, product_id):
        prices = PriceFactory(self.conn)
        price_levels = self.cursor.execute("""SELECT ID FROM PriceLevel""").fetchall()
        prices.create(product_id, price_levels)

    def set_barcode(self, product_id):
        barcode = BarcodeFactory(self.conn)
        barcode.create(product_id)

    def set_quantity(self, product_id, nums):
        quantity = QuantityFactory(self.conn)
        quantity.create(product_id, nums)

    def set_repository(self):
        repo = RepositoryFactory(self.conn)
        repo.create()

    def create(self):
        max_code = self.cursor.execute("""SELECT Max(Code) FROM KalaList""").fetchone()[0]
        max_code = 1 if max_code is None else max_code+1
        numbers = self.fake.random_number(digits=3, fix_len=False)
        params = [
            max_code, self.fake.name(), 'عدد', 0.00, 0, 0, self.get_category(), 1, 1,
            0, self.fake.text(), numbers, 1, 0, 0.00, 0.00, 0.00, 0
        ]
        self.cursor.execute("""
            INSERT INTO KalaList(
                Code, Name, Unit2, BuyPrice, SefareshPoint, Shortcut, GroupId, Active, Maliat,
                UnitType, Info, Mojoodi, MenuOrder, Weight, SellPrice, IncPerc, IncPrice, 
                ValueCalcType
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, params)
        self.cursor.commit()
        last_product_insert = self.cursor.execute("""SELECT IDENT_CURRENT('KalaList')""").fetchval()
        self.set_prices(last_product_insert)
        self.set_barcode(last_product_insert)
        self.set_quantity(last_product_insert, numbers)

    def delete(self):
        pass
        # iden = self.cursor.execute("""SELECT ID FROM KalaList""")
        # selected = random.choice(iden.fetchall())
        # product_iden_factor_detail = self.cursor.execute("""SELECT ID FROM Faktor2 WHERE IDKala = ?""", selected)
        # if product_iden_factor_detail.fetchone():
        #     return
        # self.cursor.execute("""DELETE FROM KalaList WHERE ID = ?""", selected)
        # self.cursor.commit()

    def update(self):
        iden = self.cursor.execute("""SELECT ID FROM KalaList""")
        selected = random.choice(iden.fetchall())[0]
        params = [
            self.fake.name(), self.fake.random_number(digits=2, fix_len=False), self.fake.text(), selected
        ]
        self.cursor.execute("""
            UPDATE KalaList SET Name = ?, SefareshPoint = ?, Info = ?
            WHERE ID = ?
        """, params)
        self.cursor.commit()


class BarcodeFactory(Factory):
    """Barcode Factory"""
    def create(self, product_id):
        self.cursor.execute("""
            INSERT INTO Barcode(IDKala, Text) VALUES (?, ?)
        """, (product_id, self.fake.md5()))
        self.cursor.commit()


class PriceFactory(Factory):
    """Price Factory"""
    def create(self, product_id, pricelevels=()):
        types = (1, 2)
        for type in types:
            for pricelevel in pricelevels:
                self.cursor.execute("""
                    INSERT INTO KalaPrice(PriceID, KalaID, Type, Price, [Percent], FinalPrice, Takhfif)
                    VALUES (?, ?, ?, 0.00, 0, 0.00, 0.00)
                """, (pricelevel[0], product_id, type))
        self.cursor.commit()


class QuantityFactory(Factory):
    """Quantity Factory"""

    def set_repo(self):
        rc = random.choices([True, False], [10, 1])
        if not rc:
            rf = RepositoryFactory(self.conn)
            rf.create()
        repo = self.cursor.execute("""SELECT Code FROM Negahdari""").fetchall()
        set = random.choice(repo)[0]
        return set

    def first_stock(self, product_id, nums):
        price = self.fake.random_number(digits=4)
        sum_price = float(nums * price)
        params = [
            product_id, nums, sum_price, price, self.set_repo(), 0, 0
        ]
        self.cursor.execute("""
                INSERT INTO MojodiList(IdKala, Tedad, SumPrice, Price, Anbar, Tedad1, Tedad2)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, params)
        self.cursor.commit()

    def create(self, product_id, nums):
        self.first_stock(product_id, nums)
