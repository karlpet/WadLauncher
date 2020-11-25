import os, sys, json

from core.base.Model import Model

from app.config import Config
from app.utils.Unzipper import unzip
from app.workers.DWApiWorker import api_worker_wrapper, DWApiMethod
from app.workers.DownloadWorker import download_worker_wrapper

config = Config.Instance()
wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
extensions = ['.wad', '.WAD', '.pk3', '.PK3']

def load_wad(dir):
    dir_contents = [file for file in os.listdir(dir)]
    if 'metadata.json' in dir_contents:
        with open(os.path.join(dir, 'metadata.json'), 'r') as json_file:
            return json.load(json_file)

    for file in dir_contents:
        if any((file.endswith(ext) for ext in extensions)):
            return { 'name': os.path.basename(dir), 'file': file, 'path': dir }

    return { 'name': 'ERROR, no wad found!', 'file': '' }

def wad_loader():
    return [load_wad(os.path.join(wads_path, dir)) for dir in os.listdir(wads_path)
                                                   if os.path.isdir(os.path.join(wads_path, dir))]

def save_wad(item):
    metadata_file_path = os.path.join(item['path'], 'metadata.json')
    with open(metadata_file_path, 'w+', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)

class Wads(Model):
    def __init__(self):
        Model.__init__(self, loader=wad_loader, saver=save_wad)
        self.load()
        self.wad_dir_files = []
        self.current_idgames_wad_id = None

    def select_wad(self, id):
        selected_wad = self.find(id)

        self.wad_dir_files = [file for file in os.listdir(selected_wad['path']) if file != 'saves']
        self.broadcast(('SELECT_WAD', selected_wad))

    def get_dir_contents(self):
        return self.wad_dir_files
    
    def unzip_import_wad(self, archive_file_path, item={}):
        new_wad_dir = unzip(archive_file_path)

        id = self.create(**load_wad(new_wad_dir), **item)
        self.save(id)
        self.broadcast(('CREATE_WAD', id))

    def idgames_download(self, item, mirror=None):
        id = item['id']
        progress_handlers = [
            lambda *args: self.broadcast(('DOWNLOAD_PROGRESS', (id, args)))
        ]
        download_handlers = [
            lambda _: self.broadcast(('DOWNLOAD_FINISHED', id)),
            lambda file_path: self.unzip_import_wad(file_path, item)
        ]
        download_worker_wrapper(item, progress_handlers, download_handlers, mirror)

    def idgames_random(self):
        handlers = [lambda result: self.broadcast(('RANDOM_WAD', result))]
        api_worker_wrapper(DWApiMethod.RANDOM, handlers)
    
    def idgames_get(self, wad_id):
        handlers = [lambda result: self.broadcast(('DETAIL_WAD', result))]
        api_worker_wrapper(DWApiMethod.GET, handlers, wad_id, 'id')    
    
    def idgames_search(self, text, search_by):
        handlers = [lambda result: self.broadcast(('SEARCH_WADS', result))]
        api_worker_wrapper(DWApiMethod.SEARCH, handlers, text, search_by)


sys.modules[__name__] = Wads()