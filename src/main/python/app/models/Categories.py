import sys, json, os

from core.base.Model import Model

from app.config import Config
from configparser import ConfigParser

config = Config.Instance()
BASE_PATH = os.path.expanduser(config['PATHS']['BASE_PATH'])
CATEGORIES_INI_FILE = 'user_categories.ini'
CATEGORIES_INI_PATH = os.path.join(BASE_PATH, CATEGORIES_INI_FILE)

CATEGORIES_CONFIG = ConfigParser(allow_no_value=True)
CATEGORIES_CONFIG.read(CATEGORIES_INI_PATH)

def load_categories():
    return [dict(CATEGORIES_CONFIG[c]) for c in CATEGORIES_CONFIG.sections()]

def save_category(category):
    category_id = category['id']
    if category_id not in CATEGORIES_CONFIG.sections():
        CATEGORIES_CONFIG.add_section(category_id)
    
    for key, val in category.items():
        CATEGORIES_CONFIG.set(category_id, key, val)

    with open(CATEGORIES_INI_PATH, 'w+') as categories_file:
        CATEGORIES_CONFIG.write(categories_file)

class Categories(Model):
    def __init__(self):
        Model.__init__(self, loader=load_categories, saver=save_category)
        self.load()
    
    def remove(self, id):
        self.delete(id)
        CATEGORIES_CONFIG.remove_section(id)

        with open(CATEGORIES_INI_PATH, 'w+') as categories_file:
            CATEGORIES_CONFIG.write(categories_file)

sys.modules[__name__] = Categories()