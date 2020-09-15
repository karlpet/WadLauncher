from PyQt5 import QtWidgets, QtCore, QtGui

class WadListViewModel(QtCore.QAbstractListModel):
    def __init__(self, wads = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__wads = wads

    def rowCount(self, parent):
        return len(self.__wads)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__wads[index.row()].get('name')

class WadListView:
    def __init__(self, root, wads, on_click):
        self.wad_list = root.findChild(QtWidgets.QListView, 'WadList')
        self.wad_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.wad_list.setModel(WadListViewModel(wads))
        self.wad_list.clicked.connect(lambda qindex: on_click(qindex.row()))