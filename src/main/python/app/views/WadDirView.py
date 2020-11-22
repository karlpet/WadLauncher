from PyQt5 import QtWidgets, QtCore, QtGui

class WadDirViewModel(QtCore.QAbstractListModel):
    def __init__(self, dir_files = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__dir_files = dir_files

    def rowCount(self, parent):
        return len(self.__dir_files)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__dir_files[index.row()]

class WadDirView:
    def __init__(self, root):
        self.wad_dir = root.findChild(QtWidgets.QListView, 'WadDirList')
    
    def show_dirs(self, dir_files):
        self.wad_dir.setModel(WadDirViewModel(dir_files))
