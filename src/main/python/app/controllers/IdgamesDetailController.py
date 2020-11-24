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
    
    def get_data(self, widget_index):
        if widget_index != WidgetIndices.IDGAMES_DETAIL.value:
            return
        
        wad_id = self.models.wads.get_current_idgames_wad_id()

        worker = DWApiWorker(DWApiMethod.GET, wad_id, 'id')
        worker.start()
        worker.done.connect(self.set_data)
    
    def set_data(self, response):
        result, _ = response

        self.view.setData(result)

    def download(self, id, mirror, progress_handler=None, download_handler=None):
        data = next((x for x in self.search_result if x['id'] == id), None)
        if data == None:
            return

        worker = DownloadWorker(data, mirror)
        worker.start()
        worker.progress.connect(progress_handler)
        if download_finished:
            worker.downloaded.connect(download_handler)
        worker.downloaded.connect(self.download_done)

    def download_done(self, filepath):
        self.models.wads.unzip_import_wad(filepath)

sys.modules[__name__] = IdgamesDetailController()