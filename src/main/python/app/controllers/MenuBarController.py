import sys

from app.views import MenuBarView

class MenuBarController:
    def __init__(self):
        pass
    
    def show(self, root, models):
        self.view = MenuBarView.MenuBarView(root, self)
        self.wads = models.wads
    
    def select_unzip_file(self, file_path):
        self.wads.unzip_import_wad(file_path)

sys.modules[__name__] = MenuBarController()