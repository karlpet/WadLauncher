import sys

from app.views import SearchView

from app.workers.DWApiWorker import *
from app.workers.DownloadWorker import *

class SearchController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = SearchView.SearchView(root, self)
        self.models = models
    
    def search(self, text, search_by):
        self.api_worker = DWApiWorker(DWApiMethod.SEARCH, text, search_by)
        self.api_worker.start()
        self.api_worker.done.connect(self.view.updateResults)
        self.api_worker.done.connect(self.set_search_results)

    def set_search_results(self, result_blob):
        self.search_result = result_blob.get('file', [])
        if type(self.search_result) != list:
            self.search_result = [self.search_result]


    def download(self, id, progress_indicator=None, download_finished=None):
        data = next((x for x in self.search_result if x['id'] == id), None)
        if data == None:
            return

        worker = DownloadWorker(data)
        worker.start()
        worker.progress.connect(progress_indicator)
        if download_finished:
            worker.downloaded.connect(download_finished)
        worker.downloaded.connect(self.download_done)
    

    def download_done(self, filepath):
        self.models.wads.unzip_import_wad(filepath)

sys.modules[__name__] = SearchController()