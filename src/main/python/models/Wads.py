import os

from models import Model
from config import Config


def wad_loader():
    config = Config.Instance()
    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    extensions = ['.wad', '.WAD', '.pk3']

    def load_wad(index, dir):
        print(dir)

        for file in os.listdir(os.path.join(wads_path, dir)):
            if any((file.endswith(ext) for ext in extensions)):
                return { 'id': str(index), 'name': dir, 'file': file }
        
        return { 'id': str(index), 'name': 'ERROR, no wad found!', 'file': '' }

    return [load_wad(index, dir) for index, dir in enumerate(os.listdir(wads_path))
                                 if os.path.isdir(os.path.join(wads_path, dir))]

class Wads(Model):
    def __init__(self):
        Model.__init__(self, loader=wad_loader)
        self.load()

    def select_wad(self, id):
        print(id)
        self.broadcast(('SELECT_WAD', self.find(id)))