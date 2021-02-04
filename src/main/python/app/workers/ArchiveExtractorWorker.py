import shutil, os, re, pathlib

from PyQt5.QtCore import QThread, pyqtSignal

from app.config import Config
from app.workers.WorkerPool import *

def archive_extractor_worker_wrapper(file_path, should_remove_archive=False, done_handlers=[]):
    worker = ArchiveExtractorWorker(file_path, should_remove_archive)
    for handler in done_handlers:
        worker.done.connect(handler)

    WorkerPool.Instance().start(worker)

class ArchiveExtractorWorker(QThread):
    done = pyqtSignal(str)

    def __init__(self, file_path, should_remove_archive = False, parent=None):
        QThread.__init__(self, parent)        
        self.file_path = file_path
        self.should_remove_archive = should_remove_archive

        config = Config.Instance()
        base_path = os.path.expanduser(config['PATHS']['BASE_PATH'])
        self.wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])

        # remove file extension (.zip or whatever)
        pattern = re.compile(r'\.[a-z0-9]+$')
        self.file_dir = pattern.sub('', pathlib.Path(file_path).name)
        self.temp_extraction_path = os.path.join(base_path, 'temp', self.file_dir)

    def run(self):
        pathlib.Path(self.temp_extraction_path).mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(self.file_path, self.temp_extraction_path)

        source_dir = self.temp_extraction_path
        
        tree = [f for f in os.walk(self.temp_extraction_path)][0]
        p, directories, files = tree
        # if no files are in the first level of archive extraction
        # and there exists only one directory instead
        # then we need to move the directory inside our temp_extraction_path instead.
        # this is the only case where this solution is a good idea.
        if (len(files) == 0 and len(directories) == 1):
            source_dir = os.path.join(self.temp_extraction_path, directories[0])

        destination_dir = os.path.join(self.wads_path, self.file_dir)
        shutil.move(source_dir, destination_dir)
        if source_dir != self.temp_extraction_path:
            shutil.rmtree(self.temp_extraction_path)

        if self.should_remove_archive:
            os.remove(self.file_path)

        self.done.emit(destination_dir)
