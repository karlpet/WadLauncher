from PyQt5 import uic
from PyQt5.QtWidgets import QTableView, QLineEdit
from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from app.AppContext import AppContext
from app.helpers.StackedWidgetSelector import add_widget
from app.helpers.WadItemFactory import make_wad_item, DATA_ROLE

template_path = AppContext.Instance().get_resource('template/wadtable.ui')
Form, Base = uic.loadUiType(template_path)

TABLE_ITEM_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled

class WadTableSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setFilterCaseSensitivity(False)

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        num_columns = model.columnCount()

        def get_index(i): return model.index(source_row, i, source_parent)
        def get_header(i): return model.headerData(i, Qt.Horizontal).lower()
        def get_row(i): return model.data(get_index(i))
        model_data = dict([[get_header(i), get_row(i)] for i in range(num_columns)])
        
        filter_str = self.filterRegExp().pattern()
        filter_data = {}
        for elem in filter_str.split(','):
            try:
                key, val = elem.split(':')
                filter_data[key.strip()] = val.strip()
            except ValueError:
                pass
        for key in model_data:
            if key in filter_data:
                if filter_data[key].lower() not in model_data[key].lower():
                    return False

        return True

class WadTableView(Base, Form):
    def __init__(self, root, wads, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        add_widget(root, self, 'WAD_TABLE')

        self.wads = wads
        self.proxy = WadTableSortFilterProxyModel(root)
        self.wadtable_model = QStandardItemModel()
        self.proxy.setSourceModel(self.wadtable_model)

        self.wadtable = self.findChild(QTableView, 'wadtable')
        self.wadtable.setModel(self.proxy)
        self.wadtable.selectionModel().selectionChanged.connect(self.select_item)
        self.wadtable.setSortingEnabled(True)

        self.wadtable_filter = self.findChild(QLineEdit, 'wadtable_filter')
        self.wadtable_filter.textChanged.connect(self.proxy.setFilterFixedString)

        self.keys = ['title', 'filename', 'author', 'date', 'rating']
        self.wadtable_model.setHorizontalHeaderLabels([key.capitalize() for key in self.keys])

        self.import_wads(wads.all())

    def select_item(self, selection):
        if len(selection.indexes()) == 0:
            return

        index = selection.indexes()[0]
        wad = self.wadtable.model().data(index, DATA_ROLE)

        self.wads.select_wad(wad['id'])

    def add_item(self, wad):
        item = make_wad_item(wad, TABLE_ITEM_FLAGS)
        def make_column_item(wad, key):
            return QStandardItem(wad.get(key) or 'unknown')
        column_items = [make_column_item(wad, key) for key in self.keys[1:]]
        items = [item, *column_items]

        self.wadtable_model.appendRow(items)

    def import_wads(self, wads):
        for wad in wads:
            self.add_item(wad)