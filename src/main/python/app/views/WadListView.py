from PyQt5.QtWidgets import QListView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractListModel

from app.helpers.StackedWidgetSelector import widget_changed, WidgetIndices

class WadListViewModel(QAbstractListModel):
    def __init__(self, wads = [], parent=None):
        QAbstractListModel.__init__(self, parent)
        self.__wads = wads

    def rowCount(self, parent):
        return len(self.__wads)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            wad = self.__wads[index.row()]

            return wad.get('title') or wad.get('name')
        if role == Qt.UserRole:
            return self.__wads[index.row()].get('id')

    def append(self, wad):
        self.beginResetModel()
        self.__wads.append(wad)
        self.endResetModel()

class WadListView:
    def __init__(self, root, wads):
        self.wad_list = root.findChild(QListView, 'wad_list')
        self.wads = wads

        self.wad_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.wad_list_view_model = WadListViewModel(wads.all())
        self.wad_list.setModel(self.wad_list_view_model)
        self.wad_list.selectionModel().selectionChanged.connect(self.select_item)

        widget_changed(root, self.on_widget_change)

    def on_widget_change(self, widget_index):
        if widget_index == WidgetIndices.WAD_TABLE:
            self.wad_list.hide()
        else:
            self.wad_list.show()

    def select_item(self, selection):
        index = selection.indexes()[0]
        id = self.wad_list_view_model.data(index, Qt.UserRole)

        self.wads.select_wad(id)

    def update_list(self, wad):
        self.wad_list_view_model.append(wad)
