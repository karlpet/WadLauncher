import sys

from app.views import SearchView

import app.utils.DWApi as DWApi
from app.utils.Downloader import *

class SearchController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = SearchView.SearchView(root, self)
        self.models = models
    
    def search(self, text, search_by):
        response = DWApi.search(text, search_by)
        self.result = response['file']

        self.view.updateResults(self.result)
    
    def download(self, id, progress_indicator=None):
        data = next((x for x in self.result if x['id'] == id), None)
        if data == None:
            return

        filepath = download(data, progress_indicator)
        self.models.wads.unzip_import_wad(filepath)

sys.modules[__name__] = SearchController()