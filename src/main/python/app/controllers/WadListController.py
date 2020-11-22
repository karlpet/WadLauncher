import sys

from app.views.WadListView import WadListView

class WadListController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.wads = models.wads
        self.view = WadListView(root, self.wads.all(), self.select_wad)
    
    def select_wad(self, index):
        selected_wad = self.wads.all()[index]
        
        self.wads.select_wad(selected_wad['id'])

sys.modules[__name__] = WadListController()