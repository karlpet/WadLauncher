import sys

from app.views.WadTableView import WadTableView

class WadTableController:
    def show(self, root, models):
        self.wads = models.wads
        self.view = WadTableView(root, self.wads)
        self.wads.subscribe(self.wad_subscription)

    def wad_subscription(self, msg):
        action, data = msg

        if (action == 'CREATE_WAD'):
            self.view.add_item(self.wads.find(data))

sys.modules[__name__] = WadTableController()