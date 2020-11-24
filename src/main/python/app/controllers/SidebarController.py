import sys

from app.views.SidebarView import SidebarView

class SidebarController:
    def __init__(self):
        pass

    def show(self, root, models):
        self.wads = models.wads
        self.view = SidebarView(root)

        self.wads.subscribe(self.wad_listener)
    
    def wad_listener(self, args):
        action, _ = args

        if action == 'SELECT_WAD':
            dir_files = self.wads.get_dir_contents()

            self.view.show_dirs(dir_files)

sys.modules[__name__] = SidebarController()