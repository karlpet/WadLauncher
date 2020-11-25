from PyQt5.QtWidgets import QListView, QPushButton
from PyQt5.QtCore import QAbstractListModel, Qt

from app.helpers.StackedWidgetSelector import *

class WadDirViewModel(QAbstractListModel):
    def __init__(self, dir_files = [], parent=None):
        QAbstractListModel.__init__(self, parent)
        self.__dir_files = dir_files

    def rowCount(self, parent):
        return len(self.__dir_files)
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.__dir_files[index.row()]

class SidebarView:
    def __init__(self, root, controller):
        self.wad_dir = root.findChild(QListView, 'sidebar_dirlist')
        self.search_button = root.findChild(QPushButton, 'sidebar_idgames_search')
        self.search_button.clicked.connect(lambda _: display_widget(root, WidgetIndices.IDGAMES_SEARCH))
        self.random_button = root.findChild(QPushButton, 'sidebar_idgames_random')
        self.random_button.clicked.connect(controller.random_clicked)

    def show_dirs(self, dir_files):
        self.wad_dir.setModel(WadDirViewModel(dir_files))
