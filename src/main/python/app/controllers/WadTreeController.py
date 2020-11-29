import sys

from app.views.WadTreeView import WadTreeView

class WadTreeController:
    def show(self, root, models):
        self.models = models
        self.view = WadTreeView(root, models, self)
        self.models.wads.subscribe(self.wad_subscription)
    
    def wad_subscription(self, msg):
        action, data = msg

        if (action == 'CREATE_WAD'):
            self.view.add_wad(self.models.wads.find(data))
        elif action == 'REMOVE_WAD':
            self.view.remove_wad(data)

    def remove_category(self, category):
        self.models.categories.remove(category['id'])

    def remove_wad(self, wad):
        self.models.wads.remove(wad['id'])

sys.modules[__name__] = WadTreeController()