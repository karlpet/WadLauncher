import sys

from app.views.IdgamesSearchView import IdgamesSearchView

from app.workers.DWApiWorker import *
from app.workers.DownloadWorker import *
from app.helpers.StackedWidgetSelector import *

class IdgamesSearchController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = IdgamesSearchView(root, self)
        self.models = models
        self.root = root
    
    def search(self, text, search_by):
        worker = DWApiWorker(DWApiMethod.SEARCH, text, search_by)
        worker.start()
        worker.done.connect(self.view.updateResults)
        worker.done.connect(self.set_search_results)

    def set_search_results(self, result_blob):
        self.search_result = result_blob[0].get('file', [])
        if type(self.search_result) != list:
            self.search_result = [self.search_result]
    
    def display_detail(self, wad_id):
        self.models.wads.set_current_idgames_wad_id(wad_id)
        display_widget(self.root, WidgetIndices.IDGAMES_DETAIL)

    def download(self, id, progress_handler=None, download_handler=None):
        data = next((x for x in self.search_result if x['id'] == id), None)
        if data == None:
            return

        worker = DownloadWorker(data)
        worker.start()
        worker.progress.connect(progress_handler)
        if download_handler:
            worker.downloaded.connect(download_handler)
        worker.downloaded.connect(self.download_done)
    

    def download_done(self, filepath):
        self.models.wads.unzip_import_wad(filepath)

sys.modules[__name__] = IdgamesSearchController()