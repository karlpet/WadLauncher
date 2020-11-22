from views.WadDirView import WadDirView

class WadDirController:
    def __init__(self, root, wad_model):
        self.wad_model = wad_model
        self.view = WadDirView(root)

        self.wad_model.subscribe(self.select_wad_listener)
    
    def select_wad_listener(self, args):
        action, _ = args

        if action == 'SELECT_WAD':
            dir_files = self.wad_model.get_dir_contents()

            self.view.show_dirs(dir_files)