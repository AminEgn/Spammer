# standard
import random
# internal
import connection
# faker
from faker import Faker

confs = {
    'server': '.\\Moein',
    'username': 'sa',
    'password': 'arta0@',
    'database': 'Moein'
}
conn = connection.get(**confs)

query_person_group_select = """SELECT Id FROM GroupAshkhas"""
query_person_group_insert = """INSERT INTO GroupAshkhas(parentId, caption, sms) values (?, ?, 1)"""
query_person_max_code = """SELECT Max(Code) FROM AshkhasList"""
query_person_max_id = """SELECT Max(Id) FROM AshkhasList"""
query_person_id_select = """SELECT Id FROM AshkhasList"""
query_person_delete = """DELETE FROM AshkhasList WHERE id = ?"""
query_person_insert = """
INSERT INTO AshkhasList(
code, name, fname, lname, prefix, eghtesadi, melli, site, email,
info, city, address, company, groupid, job, state, visitorperc, etebarnaghd,
buypricelevel, sellpricelevel, etebarcheque, carryprice, visitor,
visitorbed, posti, cardno, hesabno, sabt, companyaddress
)
VALUES
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0.00, ?, ?, 0.00, 0.00, 0, 0, ?, ?, ?, ?, ?)
"""
query_price_level = """SELECT ID FROM PriceLevel"""
query_person_tel_insert = """
INSERT INTO AshkhasTel(IDShakhs, Caption, tel)
VALUES 
(?, 'telephone', ?)
"""


class Factory(object):
    """Factory"""
    def __init__(self):
        self.cursor = conn.cursor()
        self.fake = Faker()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def create_more(self, n):
        for i in range(0, n):
            self.create()

    def delete_more(self, n):
        for i in range(0, n):
            self.delete()

    def update_more(self, n):
        for i in range(0, n):
            self.update()


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
            pg = PersonGroupFactory()
            pg.create()
        groups = self.cursor.execute(query_person_group_select)
        gpfetch = groups.fetchall()
        if not gpfetch:
            pg = PersonGroupFactory()
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
            params = [max_id, self.fake.random_number()]
            self.cursor.execute(query_person_tel_insert, params)
            self.cursor.commit()

    def create(self):
        max_code = self.cursor.execute(query_person_max_code).fetchone()[0]
        max_code = 1 if max_code is None else max_code+1
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        pricel_level = self.get_price_level()
        name = f'{first_name} {last_name}'
        params = [
            max_code, name, first_name, last_name, self.fake.prefix(), str(self.fake.msisdn()),
            str(self.fake.random_number()), self.fake.url(), self.fake.email(), self.fake.text(),
            self.fake.city(), self.fake.address(), self.fake.company(), self.get_group(),
            self.fake.job(), self.fake.state(), pricel_level, pricel_level, self.fake.zipcode(),
            str(self.fake.random_number()), str(self.fake.random_number()), str(self.fake.random_number()),
            self.fake.address()
        ]
        self.cursor.execute(query_person_insert, params)
        # last_id = self.cursor.fetchval()
        self.cursor.commit()
        self.person_tel(random.choice([2, 3, 4]))
        # print(f"inserted id = {last_id}")


    def delete(self):
        iden = self.cursor.execute(query_person_id_select)
        selected = random.choice(iden.fetchall())[0]
        self.cursor.execute(query_person_delete, selected)
        # deleted_id = self.cursor.fetchval()
        self.cursor.commit()
        # print(f'id {deleted_id} deleted')


if __name__ == '__main__':
    whats = input('whats you want? ')
    nums = input('how many? ')
    int_what, int_nums = int(whats), int(nums)
    pf = PersonFactory()
    if int_what == 1:
        pf.delete_more(int_nums)
    elif int_what == 2:
        pf.create_more(int_nums)
    print('finished')
