import configparser, os

DEFAULT_CONFIG = """
[WADS]
WADS_PATH = ../dev_data/wads
"""

def init_config():
    CONFIG_PATH = '../dev_data/wadlauncher_config.ini'

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    if not os.path.exists(CONFIG_PATH) or len(config.sections()) == 0:
        config.read_string(DEFAULT_CONFIG)
        with open(os.path.abspath(CONFIG_PATH), 'w+') as config_file:
            config.write(config_file)

    return config

config = init_config()