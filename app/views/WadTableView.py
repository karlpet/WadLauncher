from PyQt5 import QtWidgets

class WadTableView:
    def __init__(self, root):
        self.root = root.findChild(QtWidgets.QListWidget, 'WadList')