from views.WadTableView import WadTableView

class WadTableController:
    def __init__(self, parentView):
        self.view = WadTableView(parentView.verticalLayout, parentView.verticalLayoutWidget)