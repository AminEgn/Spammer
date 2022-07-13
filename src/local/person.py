# standard
import random
# internal
from src.local.base import Factory


query_person_group_select = """SELECT Id FROM GroupAshkhas"""
query_person_group_insert = """INSERT INTO GroupAshkhas(parentId, caption, sms) values (?, ?, 1)"""
query_person_max_code = """SELECT Max(Code) FROM AshkhasList"""
query_person_max_id = """SELECT Max(Id) FROM AshkhasList"""
query_person_id_select = """SELECT Id FROM AshkhasList"""
query_person_delete = """DELETE FROM AshkhasList WHERE id = ?"""
query_person_insert = """
INSERT INTO AshkhasList(
code, name, fname, lname, prefix, eghtesadi, melli, site, email, info, city, address,
company, groupid, job, state, visitorperc, etebarnaghd, buypricelevel, sellpricelevel,
etebarcheque, carryprice, visitor, visitorbed, posti, cardno, hesabno, sabt,
companyaddress, visitortype, peyk
)
VALUES
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.00, ?, ?, 0.00, ?, ?, 0, ?, ?, ?, ?, ?, 1, ?)
"""
query_price_level = """SELECT ID FROM PriceLevel"""
query_person_tel_insert = """
INSERT INTO AshkhasTel(IDShakhs, Caption, tel)
VALUES 
(?, 'telephone', ?)
"""


class PersonGroupFactory(Factory):
    """Person Group Factory"""
    def create(self):
        parent = 0
        have_parent = random.choices([True, False], [1, 4])
        if have_parent[0]:
            parents = self.cursor.execute(query_person_group_select)
            parentfetch = parents.fetchall()
            if parentfetch:
                parent = random.choice(parentfetch)[0]
        name = f"PersonGroup_{self.fake.company()}"
        self.cursor.execute(query_person_group_insert, [parent, name])
        self.cursor.commit()


class PersonFactory(Factory):
    """Person Factory"""
    def get_group(self):
        rc = random.choices([True, False], [1, 15])
        if rc[0]:
            pg = PersonGroupFactory(self.conn)
            pg.create()
        groups = self.cursor.execute(query_person_group_select)
        gpfetch = groups.fetchall()
        if not gpfetch:
            pg = PersonGroupFactory(self.conn)
            pg.create()
        get = random.choice(gpfetch)[0]
        return get

    def get_price_level(self):
        price_levels = self.cursor.execute(query_price_level)
        get = random.choice(price_levels.fetchall())[0]
        return get

    def person_tel(self, r):
        max_id = self.cursor.execute(query_person_max_id).fetchone()[0]
        for _ in range(1, r):
            params = [max_id, self.fake.phone_number()]
            self.cursor.execute(query_person_tel_insert, params)
            self.cursor.commit()

    def create(self):
        max_code = self.cursor.execute(query_person_max_code).fetchone()[0]
        max_code = 1 if max_code is None else max_code+1
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        pricel_level = self.get_price_level()
        name = f'{first_name} {last_name}'
        visitor = random.choices([1, 0], [1, 6])[0]
        delivery = 0
        delivery_price = 0
        if visitor:
            visitor_percent = self.fake.random_number(digits=2, fix_len=False)
        else:
            visitor_percent = 0.0
            delivery = random.choices([1, 0], [1, 6])[0]
            if delivery:
                delivery_price = self.fake.random_number(digits=4)

        params = [
            max_code,
            name,
            first_name,
            last_name,
            self.fake.prefix(),
            str(self.fake.random_number(digits=10)),
            str(self.fake.random_number(digits=11)),
            self.fake.url(),
            self.fake.email(),
            self.fake.text(),
            self.fake.city(),
            self.fake.address(),
            self.fake.company(),
            self.get_group(),
            self.fake.job(),
            self.fake.state(),
            visitor_percent,
            pricel_level,
            pricel_level,
            delivery_price,
            visitor,
            str(self.fake.zipcode()),
            str(self.fake.random_number(digits=16)),
            str(self.fake.random_number(digits=14)),
            str(self.fake.random_number(digits=8)),
            self.fake.address(),
            delivery
        ]
        self.cursor.execute(query_person_insert, params)
        self.cursor.commit()
        self.person_tel(random.choice([2, 3, 4]))

    def delete(self):
        iden = self.cursor.execute(query_person_id_select)
        selected = random.choice(iden.fetchall())[0]
        self.cursor.execute(query_person_delete, selected)
        self.cursor.commit()

    def update(self):
        iden = self.cursor.execute(query_person_id_select)
        selected = random.choice(iden.fetchall())[0]
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        name = f'{first_name} {last_name}'
        params = [
            first_name, last_name, name, self.fake.job(), self.fake.city(), self.fake.url(),
            self.fake.email(), selected
        ]
        self.cursor.execute("""
            UPDATE AshkhasList SET fname = ?, lname = ?, name = ?, job = ?, city = ?,
            site = ?, email = ?
            WHERE ID = ?
        """, params)
        self.cursor.commit()
