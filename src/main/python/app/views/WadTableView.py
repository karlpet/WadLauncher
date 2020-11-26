from PyQt5 import uic
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel

from app.AppContext import AppContext
from app.helpers.StackedWidgetSelector import add_widget

template_path = AppContext.Instance().get_resource('template/wadtable.ui')
Form, Base = uic.loadUiType(template_path)

class WadTableModel(QAbstractTableModel):
    def __init__(self, wads):
        super(self.__class__, self).__init__()
        self.__wads = wads
        self.keys = ['title', 'filename', 'author', 'date', 'rating']

    def data(self, index, role):
        wad = self.__wads[index.row()]

        if role == Qt.DisplayRole:
            key = self.keys[index.column()]
            if key == 'title':
                return wad.get(key) or wad['name']
            return wad.get(key) or 'unknown'
        if role == Qt.UserRole:
            return wad['id']

    def rowCount(self, index):
        return len(self.__wads)
    
    def columnCount(self, index):
        return len(self.keys)

class WadTableView(Base, Form):
    def __init__(self, root, wads, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        add_widget(root, self, 'WAD_TABLE')

        self.wadtable = self.findChild(QTableView, 'wadtable')
        self.wadtable.setModel(WadTableModel(wads))
