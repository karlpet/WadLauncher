import os

from PyQt5.QtWidgets import QTreeView, QPushButton, QFileSystemModel
from PyQt5.QtCore import QAbstractListModel, Qt, QDir

from app.helpers.StackedWidgetSelector import display_widget, WidgetIndices

class SidebarView:
    def __init__(self, root, controller):
        self.wad_dir_model = QFileSystemModel()
        self.wad_dir = root.findChild(QTreeView, 'sidebar_waddir')
        self.wad_dir.setModel(self.wad_dir_model)
        for i in range(1, self.wad_dir.header().length()):
            self.wad_dir.hideColumn(i)
        
        self.search_button = root.findChild(QPushButton, 'sidebar_idgames_search')
        def search(): display_widget(root, WidgetIndices.IDGAMES_SEARCH)
        self.search_button.clicked.connect(search)

        self.random_button = root.findChild(QPushButton, 'sidebar_idgames_random')
        self.random_button.clicked.connect(controller.random_clicked)

        self.wadtable_button = root.findChild(QPushButton, 'sidebar_wadsview_table')
        def wadtable(): display_widget(root, WidgetIndices.WAD_TABLE)
        self.wadtable_button.clicked.connect(wadtable)

        self.wadtree = root.findChild(QPushButton, 'sidebar_wadsview_tree')
        def wadtable(): display_widget(root, WidgetIndices.WAD_TREE)
        self.wadtree.clicked.connect(wadtable)


    def show_dir(self, path):
        self.wad_dir_model.setRootPath(QDir.currentPath())
        self.wad_dir.setRootIndex(self.wad_dir_model.index(path))
