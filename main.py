# standard
import random
import time
# internal
from src import connection
from src.local.product import ProductFactory
from src.local.person import PersonFactory
from src.server.invoices import InvoiceWebFactory
from src.local.portions import PortionFactory


confs = {
    'server': '.\\Moein',
    'username': 'sa',
    'password': 'arta0@',
    'database': 'Moein'
}
conn = connection.get(**confs)

HEADERS = {
    'Authorization': "Token 1b53627f436cd58ae74aa7764f164bb6f0d462b1"
}
URL = 'http://127.0.0.1:8000'

person = PersonFactory(conn)
product = ProductFactory(conn)
invoice = InvoiceWebFactory(conn, URL, HEADERS)
portion = PortionFactory(conn)

factories = (
    person,
    product,
    invoice,
    portion,
)

track_tuple_key = (
    'Person',
    'Product',
    'Invoice',
    'Portion'
)
track_tuple_value = (
    'COUNT',
    'DELETE',
    'INSERT',
    'UPDATE',
)


track_dict = dict.fromkeys(track_tuple_key, None)
for k in track_dict.keys():
    track_dict[k] = dict.fromkeys(track_tuple_value, 0)


def first_time():
    for i, factory in enumerate(factories):
        if i < 2:
            nums = 50
        else:
            nums = 10
        factory.create_more(nums)


def main(timesleep):
    while True:
        how_many = random.randint(1, 8)
        what_to_do = random.choices([1, 2, 3], [1, 5, 2])[0]
        chosen = random.choices([0, 1, 2, 3], [10, 10, 5, 2])[0]
        table = factories[chosen]
        table_name = track_tuple_key[chosen]
        act = track_tuple_value[what_to_do]
        try:
            if what_to_do == 1:
                table.delete_more(how_many)
            elif what_to_do == 3:
                table.update_more(how_many)
            else:
                table.create_more(how_many)

            n = track_dict.get(table_name).get(act)
            track_dict[table_name][act] = n + how_many
            nums = track_dict.get(table_name).get('COUNT')
            if act == 'DELETE':
                track_dict[table_name]['COUNT'] = nums - how_many

            elif act == 'INSERT':
                track_dict[table_name]['COUNT'] = nums + how_many

        except Exception as e:
            print(str(e))

        print(
            f'{how_many} {act} in table {table_name}\n',
              track_dict[table_name],'\n'
            )
        time.sleep(timesleep)


if __name__ == '__main__':
    time_interval = int(input('how much time sleep? '))
    ft = True
    if ft:
        print('first time activated')
        first_time()
    main(time_interval)
