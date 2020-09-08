from PyQt5 import QtWidgets

class WadListView:
    def __init__(self, root, wads, select_wad):
        self.root = root.findChild(QtWidgets.QListWidget, 'WadList')

        self.root.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.root.addItems(wads)
        self.root.itemSelectionChanged.connect(lambda: select_wad(self.get_selected_index()))

    def get_selected_index(self):
        try:
            return self.root.selectedIndexes()[0].row()
        except IndexError:
            return -1