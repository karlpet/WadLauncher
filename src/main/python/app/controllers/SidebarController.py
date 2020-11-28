import sys

from app.views.SidebarView import SidebarView

class SidebarController:
    def __init__(self):
        pass

    def show(self, root, models):
        self.wads = models.wads
        self.view = SidebarView(root, self)
        self.root = root
        self.wads.subscribe(self.wad_listener)
    
    def wad_listener(self, args):
        action, data = args

        if action == 'SELECT_WAD':
            self.view.show_dir(data['path'])
 
    def random_clicked(self):
        self.wads.idgames_random()

sys.modules[__name__] = SidebarController()