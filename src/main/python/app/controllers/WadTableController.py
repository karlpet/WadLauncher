import sys

from app.views.WadTableView import WadTableView

class WadTableController:
    def show(self, root, models):
        self.wads = models.wads
        self.view = WadTableView(root, self.wads)

sys.modules[__name__] = WadTableController()