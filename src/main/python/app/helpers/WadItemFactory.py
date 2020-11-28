from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

DATA_ROLE = Qt.UserRole + 1

def make_wad_item(wad, flags):
    string = wad.get('title') or wad.get('name')

    item = QStandardItem(string)
    item.setFlags(flags)
    item.setData(wad, DATA_ROLE)
    return item
