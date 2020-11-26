from PyQt5 import uic
from PyQt5.QtWidgets import QTableView, QLineEdit
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QItemSelectionModel, QSortFilterProxyModel

from app.AppContext import AppContext
from app.helpers.StackedWidgetSelector import add_widget

template_path = AppContext.Instance().get_resource('template/wadtable.ui')
Form, Base = uic.loadUiType(template_path)

class WadTableModel(QAbstractTableModel):
    def __init__(self, wads):
        super(self.__class__, self).__init__()
        self.wads = wads
        self.__wads = wads.all()
        self.keys = ['Title', 'Filename', 'Author', 'Date', 'Rating']

    def data(self, index, role=Qt.DisplayRole):
        wad = self.__wads[index.row()]

        if role == Qt.DisplayRole:
            key = self.keys[index.column()].lower()
            if key == 'title':
                return wad.get(key) or wad['name']
            return wad.get(key) or 'unknown'
        if role == Qt.UserRole:
            return wad['id']

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.keys[section]

    def rowCount(self, index):
        return len(self.__wads)
    
    def columnCount(self, index):
        return len(self.keys)

class WadTableSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setFilterCaseSensitivity(False)

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        num_columns = model.columnCount(source_row)

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
        self.proxy.setSourceModel(WadTableModel(wads))

        self.wadtable = self.findChild(QTableView, 'wadtable')
        self.wadtable.setModel(self.proxy)
        self.wadtable.selectionModel().selectionChanged.connect(self.select_item)
        self.wadtable.setSortingEnabled(True)

        self.wadtable_filter = self.findChild(QLineEdit, 'wadtable_filter')
        self.wadtable_filter.textChanged.connect(self.proxy.setFilterFixedString)

    def select_item(self, selection):
        index = selection.indexes()[0]
        id = self.wadtable.model().data(index, Qt.UserRole)

        self.wads.select_wad(id)
