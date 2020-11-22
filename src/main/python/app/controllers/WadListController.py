import sys

from app.views.WadListView import WadListView

class WadListController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.wads = models.wads
        self.view = WadListView(root, self.wads)

        self.wads.subscribe(self.wad_subscription)
    
    def wad_subscription(self, msg):
        action, data = msg

        if (action == 'CREATE_WAD'):
            self.view.update_list(self.wads.find(data))

sys.modules[__name__] = WadListController()