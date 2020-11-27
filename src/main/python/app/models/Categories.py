import sys, json, os

from core.base.Model import Model

from app.config import Config
from configparser import ConfigParser

def load_categories():
    config = Config.Instance()
    BASE_PATH = os.path.expanduser(config['PATHS']['BASE_PATH'])
    CATEGORIES_INI_FILE = 'user_categories.ini'
    CATEGORIES_INI_PATH = os.path.join(BASE_PATH, CATEGORIES_INI_FILE)

    categories_config = ConfigParser(allow_no_value=True)
    categories_config.read(CATEGORIES_INI_PATH)

    return [dict(categories_config[c]) for c in categories_config.sections()]

def save_category(category):
    config = Config.Instance()
    BASE_PATH = os.path.expanduser(config['PATHS']['BASE_PATH'])
    CATEGORIES_INI_FILE = 'user_categories.ini'
    CATEGORIES_INI_PATH = os.path.join(BASE_PATH, CATEGORIES_INI_FILE)

    categories_config = ConfigParser(allow_no_value=True)
    categories_config.read(CATEGORIES_INI_PATH)

    category_id = category['id']
    if category_id not in categories_config.sections():
        categories_config.add_section(category_id)
    
    for key, val in category.items():
        categories_config.set(category_id, key, val)

    with open(CATEGORIES_INI_PATH, 'w+') as categories_file:
        categories_config.write(categories_file)

class Categories(Model):
    def __init__(self):
        Model.__init__(self, loader=load_categories, saver=save_category)
        self.load()

sys.modules[__name__] = Categories()