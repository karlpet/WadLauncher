import os, sys

from core.base.Model import Model
from app.config import Config

def wad_loader():
    config = Config.Instance()
    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    extensions = ['.wad', '.WAD', '.pk3']

    def load_wad(index, dir):
        for file in os.listdir(os.path.join(wads_path, dir)):
            if any((file.endswith(ext) for ext in extensions)):
                return { 'id': str(index), 'name': dir, 'file': file, 'path': os.path.join(wads_path, dir) }
        
        return { 'id': str(index), 'name': 'ERROR, no wad found!', 'file': '' }

    return [load_wad(index, dir) for index, dir in enumerate(os.listdir(wads_path))
                                 if os.path.isdir(os.path.join(wads_path, dir))]

class Wads(Model):
    def __init__(self):
        Model.__init__(self, loader=wad_loader)
        self.load()
        self.wad_dir_files = []

    def select_wad(self, id):
        selected_wad = self.find(id)

        self.wad_dir_files = [file for file in os.listdir(selected_wad['path']) if file != 'saves']
        self.broadcast(('SELECT_WAD', selected_wad))
    
    def get_dir_contents(self):
        return self.wad_dir_files

sys.modules[__name__] = Wads()