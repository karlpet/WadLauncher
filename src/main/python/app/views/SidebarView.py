import os

from PyQt5.QtWidgets import QTreeView, QPushButton, QFileSystemModel, QListView
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from app.helpers.StackedWidgetSelector import display_widget, WidgetIndices

PATH_ROLE = Qt.UserRole + 1

class SidebarView:
    def __init__(self, root, controller):
        self.wad_dir_model = QFileSystemModel()
        self.wad_dir = root.findChild(QTreeView, 'sidebar_waddir')
        self.wad_dir.setModel(self.wad_dir_model)
        for i in range(1, self.wad_dir.header().length()):
            self.wad_dir.hideColumn(i)
        
        self.loadorder_model = QStandardItemModel()
        self.loadorder = root.findChild(QListView, 'sidebar_loadorder')
        self.loadorder.setModel(self.loadorder_model)

        self.search_button = root.findChild(QPushButton, 'sidebar_idgames_search')
        def search(): display_widget(root, WidgetIndices.IDGAMES_SEARCH)
        self.search_button.clicked.connect(search)

        self.random_button = root.findChild(QPushButton, 'sidebar_idgames_random')
        self.random_button.clicked.connect(controller.random_clicked)

    def show_dir(self, wad):
        self.wad_dir_model.setRootPath(QDir.currentPath())
        self.wad_dir.setRootIndex(self.wad_dir_model.index(wad['path']))
        self.selected_path = wad['path']

        try:
            self.loadorder_model.clear()
            for file_path in wad['file_paths']:
                file_name = os.path.basename(file_path)
                item = QStandardItem(file_name)
                item.setData(file_path, PATH_ROLE)
                self.loadorder_model.appendRow(item)
        except KeyError:
            print('file paths not found in:', wad['name'])
