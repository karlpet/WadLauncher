import sys

from app.views.IdgamesDetailView import IdgamesDetailView

from app.workers.DWApiWorker import *
from app.workers.DownloadWorker import *
from app.helpers.StackedWidgetSelector import *

class IdgamesDetailController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.root = root
        self.models = models
        self.view = IdgamesDetailView(root, self)
        self.models.wads.subscribe(self.wads_listener)
    
    def wads_listener(self, args):
        action, data = args

        if action in ['RANDOM_WAD', 'DETAIL_WAD']:
            result, err = data
            self.data = result
            self.view.set_data(result)
            display_widget(self.root, WidgetIndices.IDGAMES_DETAIL)

    def download(self, mirror, progress_handler=None, download_handler=None):
        if self.data == None:
            return

        worker = DownloadWorker(self.data, mirror)
        worker.start()
        worker.progress.connect(progress_handler)
        if download_handler:
            worker.downloaded.connect(download_handler)
        worker.downloaded.connect(self.download_done)

    def download_done(self, filepath):
        self.models.wads.unzip_import_wad(filepath)

sys.modules[__name__] = IdgamesDetailController()