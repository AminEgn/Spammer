# standard
import json
# internal
from src.confs import SETTINGS_FILE, APP_SETTINGS


class API(object):
    """Settings API"""
    def __init__(self):
        self._settings = dict()
        self._open_setting()

    def _open_setting(self):
        try:
            with open(SETTINGS_FILE, 'rt') as f:
                settings = json.loads(f.read())
                for key, value in settings.items():
                        self._settings[key] = value

        except Exception as e:
            print(str(e))
            self._settings = APP_SETTINGS

    def get_setting(self, key, default=None):
        return self._settings.get(key, default)

    def set_setting(self, key, value):
        self._settings[key] = value

    def save_setting(self):
        with open(SETTINGS_FILE, 'wt') as f:
            f.write(json.dumps(self._settings, indent=4))

    def reload(self):
        self._open_setting()


# instance
_api = API()

# interface
# - read
r = _api.get_setting
# - write
w = _api.set_setting
# - save
s = _api.save_setting
# - reload
reload = _api.reload