import os, sys, json, shutil

from core.base.Model import Model

from app.config import Config
from app.workers.DWApiWorker import api_worker_wrapper, DWApiMethod
from app.workers.DownloadWorker import download_worker_wrapper
from app.workers.ArchiveExtractorWorker import archive_extractor_worker_wrapper

config = Config.Instance()
WADS_PATH = os.path.expanduser(config['PATHS']['WADS_PATH'])
EXTENSIONS = ['.wad', '.pk3', '.deh', '.bex']


def is_mod(file): return any(file.lower().endswith(ext) for ext in EXTENSIONS)


def search_wad_dir(dir):
    file_paths = []
    for (root, _, files) in os.walk(dir):
        file_paths.extend(
            [os.path.join(root, file) for file in files if is_mod(file)]
        )
    return file_paths


def load_wad(dir):
    if 'metadata.json' in os.listdir(dir):
        with open(os.path.join(dir, 'metadata.json'), 'r') as json_file:
            return json.load(json_file)
    loaded_wad = {
        'name': os.path.basename(dir),
        'path': dir,
        'file_paths': search_wad_dir(dir)
    }
    try:
        loaded_wad.update(file_path=loaded_wad['file_paths'][0])
    except IndexError:
        loaded_wad.update(file_path=None, error='No mod file found (.wad or .pk3)')
    return loaded_wad


def wad_loader():
    return [load_wad(os.path.join(WADS_PATH, dir)) for dir in os.listdir(WADS_PATH)
                                                   if os.path.isdir(os.path.join(WADS_PATH, dir))]


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

        self.broadcast(('SELECT_WAD', selected_wad))

    def extract_archive(self, file_path, should_remove_archive=False, item={}):
        done_handlers = [
            lambda wad_dir: self.import_wad(wad_dir, item)
        ]
        archive_extractor_worker_wrapper(file_path, should_remove_archive, done_handlers)

    def import_wad(self, wad_dir, item={}):
        id = self.create(**load_wad(wad_dir), **item)
        self.save(id)
        self.broadcast(('CREATE_WAD', id))

    def idgames_download(self, item, mirror=None):
        id = item['id']
        progress_handlers = [
            lambda *args: self.broadcast(('DOWNLOAD_PROGRESS', (id, args)))
        ]
        download_handlers = [
            lambda _: self.broadcast(('DOWNLOAD_FINISHED', id)),
            lambda file_path: self.extract_archive(file_path, True, item)
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
    
    def remove(self, id):
        wad = self.delete(id)
        self.broadcast(('REMOVE_WAD', wad))
        shutil.rmtree(wad['path'])


sys.modules[__name__] = Wads()