import os

from models import Model
from config import Config

def wad_loader():
    config = Config.Instance()
    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    
    return [{ 'id': str(index), 'name': dir, 'file': dir + '.wad'} for index, dir in enumerate(os.listdir(wads_path))
                if os.path.isdir(os.path.join(wads_path, dir))]

class Wads(Model):
    def __init__(self):
        Model.__init__(self, loader=wad_loader)
        self.load()

    def select_wad(self, id):
        print(id)
        self.broadcast(('SELECT_WAD', self.find(id)))