from PyQt5.QtCore import QAbstractListModel, Qt

class ComboBoxModel(QAbstractListModel):
    def __init__(self, contents = [], display_key=None, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.contents = contents
        self.display_key = display_key

    def rowCount(self, parent):
        return len(self.contents)

    def data(self, index, role):
        item = self.contents[index.row()]

        if role == Qt.DisplayRole:
            if type(item) == dict:
                return item.get(self.display_key)
            return item
        if role == Qt.UserRole and type(item) == dict:
            return item.get('id')
