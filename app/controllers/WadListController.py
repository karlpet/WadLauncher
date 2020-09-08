from views.WadListView import WadListView

class WadListController:
    def __init__(self, root, wad_model):
        self.view = WadListView(root, wad_model.get_wads(), wad_model.select_wad)