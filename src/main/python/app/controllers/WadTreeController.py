import sys

from app.views.WadTreeView import WadTreeView

class WadTreeController:
    def show(self, root, models):
        self.view = WadTreeView(root, models)

sys.modules[__name__] = WadTreeController()