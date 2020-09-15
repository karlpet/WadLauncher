import glob, os, functools

from models import Model
from config import Config

def iwad_loader():
    config = Config.Instance()
    path = os.path.expanduser(config['PATHS']['IWADS_PATH'])
    files = glob.glob(os.path.join(os.path.abspath(path), '*.wad'))

    iwads = []
    for file in files:
        with open(file, 'rb') as fd:
            wad_type = fd.read(4).decode("utf-8")
            if wad_type == 'IWAD':
                iwads.append({'name': os.path.basename(file),
                              'path': file})

    return iwads

class Iwads(Model):
    def __init__(self):
        Model.__init__(self, loader=iwad_loader)
        self.load()
