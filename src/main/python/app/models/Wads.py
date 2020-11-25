import os, sys

from core.base.Model import Model
from app.config import Config
from app.utils.Unzipper import unzip
from app.workers.DWApiWorker import *

config = Config.Instance()
wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
extensions = ['.wad', '.WAD', '.pk3', '.PK3']

def load_wad(dir):
    for file in os.listdir(dir):
        if any((file.endswith(ext) for ext in extensions)):
            return { 'name': os.path.basename(dir), 'file': file, 'path': dir }
    
    return { 'name': 'ERROR, no wad found!', 'file': '' }

def wad_loader():
    return [load_wad(os.path.join(wads_path, dir)) for dir in os.listdir(wads_path)
                                                   if os.path.isdir(os.path.join(wads_path, dir))]

class Wads(Model):
    def __init__(self):
        Model.__init__(self, loader=wad_loader)
        self.load()
        self.wad_dir_files = []
        self.current_idgames_wad_id = None

    def select_wad(self, id):
        selected_wad = self.find(id)

        self.wad_dir_files = [file for file in os.listdir(selected_wad['path']) if file != 'saves']
        self.broadcast(('SELECT_WAD', selected_wad))

    def get_dir_contents(self):
        return self.wad_dir_files
    
    def unzip_import_wad(self, file_path):
        new_wad_dir = unzip(file_path)

        id = self.create(**load_wad(new_wad_dir))
        self.broadcast(('CREATE_WAD', id))
    
    def get_random_wad(self):
        worker = DWApiWorker(DWApiMethod.RANDOM)
        worker.start()
        worker.done.connect(lambda result: self.broadcast(('RANDOM_WAD', result)))
    
    def get_wad_detail(self, wad_id):
        worker = DWApiWorker(DWApiMethod.GET, wad_id, 'id')
        worker.start()
        worker.done.connect(lambda result: self.broadcast(('DETAIL_WAD', result)))
    


sys.modules[__name__] = Wads()