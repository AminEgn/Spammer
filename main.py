# standard
import random
import time
# internal
from src import connection
from src.product import ProductFactory
from src.person import PersonFactory
from src.product import QuantityFactory


confs = {
    'server': '.\\Moein',
    'username': 'sa',
    'password': 'arta0@',
    'database': 'Moein'
}
conn = connection.get(**confs)

product = ProductFactory(conn)
person = PersonFactory(conn)


if __name__ == '__main__':
    time_inter = int(input('how much time sleep? '))
    first_time = True
    action_nums = {
        'Product': {
            'DELETE': 0,
            'INSERT': 0,
            'UPDATE': 0,
            'COUNT': 0
        },
        'Person': {
            'DELETE': 0,
            'INSERT': 0,
            'UPDATE': 0,
            'COUNT': 0
        }
    }
    while True:
        table_name = ''
        how_many = random.randint(1, 11)
        what_to_do = random.choices([1, 2, 3], [1, 5, 2])[0]
        chosen = random.choice([1, 2])
        if chosen == 1:
            table_name = 'Person'
            table = person
        elif chosen == 2:
            table_name = 'Product'
            table = product

        if first_time:
            how_many = 12
            what_to_do = 2
        nums = action_nums.get(table_name).get('COUNT')
        try:
            if what_to_do == 1:
                act = 'DELETE'
                table.delete_more(how_many)
            elif what_to_do == 3:
                act = 'UPDATE'
                table.update_more(how_many)
            else:
                act = 'INSERT'
                table.create_more(how_many)
            n = action_nums.get(table_name).get(act)
            action_nums[table_name][act] = n + how_many

            if act == 'DELETE':
                action_nums[table_name]['COUNT'] = nums - how_many
            elif act == 'INSERT':
                action_nums[table_name]['COUNT'] = nums + how_many

        except Exception as e:
            print(str(e))

        first_time = False
        print(
            f'{how_many} {act} in table {table_name}\n',
              action_nums[table_name],'\n'
            )
        time.sleep(time_inter)
