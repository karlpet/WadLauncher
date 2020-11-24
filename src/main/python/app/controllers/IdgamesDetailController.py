import sys

from app.views import IdgamesDetailView

from app.workers.DWApiWorker import *
from app.workers.DownloadWorker import *
from app.helpers.StackedWidgetSelector import WidgetIndices

class IdgamesDetailController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = IdgamesDetailView.IdgamesDetailView(root, self)
        self.models = models
        self.models.wads.subscribe(self.wads_listener)
    
    def wads_listener(self, args):
        action, data = args

        if action == 'RANDOM_WAD':
            result, _ = data
            self.data = result
            self.view.setData(result)
    
    def get_data(self, widget_index):
        if widget_index != WidgetIndices.IDGAMES_DETAIL.value:
            return
        
        wad_id = self.models.wads.get_current_idgames_wad_id()

        worker = DWApiWorker(DWApiMethod.GET, wad_id, 'id')
        worker.start()
        worker.done.connect(self.set_data)
    
    def set_data(self, response):
        result, _ = response

        self.data = result
        self.view.setData(result)

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