# standard
import random
# internal
from src.server import req
from src.server.base import Factory


class PersonWebFactory(Factory):
    """Person Web Factory"""
    def _post(self, url, params):
        res = req.post(f'{url}/api/temp_persons', json=params, headers=self.headers)
        return res

    def get_pricelevel(self):
        pass

    def get_group(self):
        pass

    def gen_tels(self):
        person_tel = PersonTelWebFactory()
        c = random.choice([2, 3, 4])
        tels = list()
        for _ in range(1, c):
            tels.append(person_tel.create())
        return tels

    def create(self):
        params = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'name_prefix': self.fake.prefix(),
            'city': self.fake.city(),
            'province': self.fake.state(),
            'company': self.fake.company(),
            'tels': self.gen_tels()
        }
        self._post(self.url, params)


class PersonTelWebFactory(Factory):
    """Person Tel Web Factory"""
    def create(self):
        caption = random.choice(['mobile', 'fax', 'telephone', 'home'])
        params = {
            'tel': str(self.fake.phone_number()),
            'caption': caption,
        }
        return params
