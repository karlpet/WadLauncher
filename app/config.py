import configparser, os
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox

from utils.decorators import Singleton

DEFAULT_CONFIG = """
[PATHS]
WADS_PATH = ../dev_data/wads
IWADS_PATH =
"""

@Singleton
class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        
        CONFIG_DIRECTORY = '../dev_data'
        CONFIG_PATH = os.path.join(CONFIG_DIRECTORY, 'wadlauncher_config.ini')

        Path(CONFIG_DIRECTORY).mkdir(parents=True, exist_ok=True)
        self.read(CONFIG_PATH)

        if not os.path.exists(CONFIG_PATH) or len(self.sections()) == 0:
            self.read_string(DEFAULT_CONFIG)
            with open(os.path.abspath(CONFIG_PATH), 'w+') as config_file:
                self.write(config_file)
        
        if self['PATHS']['IWADS_PATH'] == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle('Path to iwads not found')
            msgBox.setText('To play pwads, you need an iwad as a base.\nSpecify a path to the iwad directory in\n"' + CONFIG_PATH + '".')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()