import sys

from app.views import SearchView

class SearchController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = SearchView.SearchView(root)

sys.modules[__name__] = SearchController()