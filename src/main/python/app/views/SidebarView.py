from PyQt5 import QtWidgets, QtCore, QtGui

from app.helpers.StackedWidgetSelector import *

class WadDirViewModel(QtCore.QAbstractListModel):
    def __init__(self, dir_files = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__dir_files = dir_files

    def rowCount(self, parent):
        return len(self.__dir_files)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__dir_files[index.row()]

class SidebarView:
    def __init__(self, root, controller):
        self.wad_dir = root.findChild(QtWidgets.QListView, 'sidebar_dirlist')
        self.search_button = root.findChild(QtWidgets.QPushButton, 'sidebar_idgames_search')
        self.search_button.clicked.connect(lambda _: display_widget(root, WidgetIndices.IDGAMES_SEARCH))
        self.random_button = root.findChild(QtWidgets.QPushButton, 'sidebar_idgames_random')
        self.random_button.clicked.connect(controller.random_clicked)

    def show_dirs(self, dir_files):
        self.wad_dir.setModel(WadDirViewModel(dir_files))
