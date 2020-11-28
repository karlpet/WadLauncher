from PyQt5.QtWidgets import QListView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractListModel
from PyQt5.QtGui import QStandardItemModel

from app.helpers.StackedWidgetSelector import widget_changed, WidgetIndices
from app.helpers.WadItemFactory import make_wad_item, DATA_ROLE

LIST_ITEM_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled

class WadListView:
    def __init__(self, root, wads):
        self.wadlist = root.findChild(QListView, 'wad_list')
        self.wads = wads
        self.wadlist_model = QStandardItemModel()
        self.wadlist.setModel(self.wadlist_model)
        self.wadlist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.wadlist.selectionModel().selectionChanged.connect(self.select_item)
        self.import_wads(wads.all())

        widget_changed(root, self.on_widget_change)

    def on_widget_change(self, widget_index):
        if widget_index in [WidgetIndices.WAD_TABLE, WidgetIndices.WAD_TREE]:
            self.wadlist.hide()
        else:
            self.wadlist.show()

    def select_item(self, selection):
        index = selection.indexes()[0]
        item = self.wadlist_model.data(index, DATA_ROLE)

        self.wads.select_wad(item['id'])

    def add_item(self, wad):
        item = make_wad_item(wad, LIST_ITEM_FLAGS)

        self.wadlist_model.appendRow(item)

    def import_wads(self, wads):
        for wad in wads:
            self.add_item(wad)
