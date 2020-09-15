from views.WadListView import WadListView

class WadListController:
    def __init__(self, root, wad_model):
        self.wad_model = wad_model
        self.view = WadListView(root, wad_model.all(), self.select_wad)
    
    def select_wad(self, index):
        selected_wad = self.wad_model.all()[index]
        
        self.wad_model.select_wad(selected_wad['id'])
