import sys, os

from core.base.Model import Model

from app.config import Config
from configparser import ConfigParser

config = Config.Instance()
BASE_PATH = os.path.expanduser(config['PATHS']['BASE_PATH'])
SOURCE_PORTS_INI_PATH = os.path.join(BASE_PATH, 'source_ports.ini')
SOURCE_PORTS_CONFIG = ConfigParser(allow_no_value=True)
SOURCE_PORTS_CONFIG.read(SOURCE_PORTS_INI_PATH)

def source_port_loader():
    source_ports = []
    sections = SOURCE_PORTS_CONFIG.sections()

    for section in sections:
        source_ports.append(SOURCE_PORTS_CONFIG[section])

    return source_ports

class SourcePorts(Model):
    def __init__(self):
        Model.__init__(self, loader=source_port_loader)
        self.load()

sys.modules[__name__] = SourcePorts()