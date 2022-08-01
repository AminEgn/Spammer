# standard
import os


# application info
APP_NAME = 'Spammer'
APP_VERSION = 1.0
APP_AUTHOR = 'M.Amin Eidgahian'

# base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# settings file
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.json')

# default settings
APP_SETTINGS = {
    'database_server':   '',
    'database_username': '',
    'database_password': '',
    'database_name':     '',
    'api_token':         '',
    'api_domain':        ''
}
