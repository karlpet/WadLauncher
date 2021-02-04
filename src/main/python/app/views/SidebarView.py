import os

from PyQt5.QtWidgets import QTreeView, QPushButton, QFileSystemModel, QListView
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from app.helpers.StackedWidgetSelector import display_widget, WidgetIndices

PATH_ROLE = Qt.UserRole + 1
LOAD_ORDER_ITEM_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled

class SidebarView:
    def __init__(self, root, wads, controller):
        self.wads = wads

        self.wad_dir_model = QFileSystemModel()
        self.wad_dir = root.findChild(QTreeView, 'sidebar_waddir')
        self.wad_dir.setModel(self.wad_dir_model)
        for i in range(1, self.wad_dir.header().length()):
            self.wad_dir.hideColumn(i)
        
        self.loadorder_model = QStandardItemModel()
        # rowsRemoved is called when something is moved, AFTER the model actually is updated
        self.loadorder_model.rowsRemoved.connect(self.manual_ordering)
        self.loadorder = root.findChild(QListView, 'sidebar_loadorder')
        self.loadorder.setModel(self.loadorder_model)
        self.loadorder.clicked.connect(self.manual_ordering)

        self.search_button = root.findChild(QPushButton, 'sidebar_idgames_search')
        def search(): display_widget(root, WidgetIndices.IDGAMES_SEARCH)
        self.search_button.clicked.connect(search)

        self.random_button = root.findChild(QPushButton, 'sidebar_idgames_random')
        self.random_button.clicked.connect(controller.random_clicked)
        self.selected_wad_id = None

    def show_dir(self, wad):
        self.wad_dir_model.setRootPath(QDir.currentPath())
        self.wad_dir.setRootIndex(self.wad_dir_model.index(wad['path']))
        self.selected_path = wad['path']
        self.selected_wad_id = wad['id']

        try:
            self.loadorder_model.clear()
            for file_path in wad['file_paths']:
                file_name = os.path.basename(file_path)
                item = QStandardItem(file_name)
                item.setData(file_path, PATH_ROLE)
                item.setFlags(LOAD_ORDER_ITEM_FLAGS)
                item.setCheckable(True)
                item.setCheckState(Qt.Checked)
                self.loadorder_model.appendRow(item)
        except KeyError:
            print('file paths not found in:', wad['name'])

    def manual_ordering(self, *_):
        file_paths_reordered = []
        for i in range(self.loadorder_model.rowCount()):
            item = self.loadorder_model.item(i)
            if item.checkState() == Qt.Checked:
                file_paths_reordered.append(item.data(PATH_ROLE))

        self.wads.set_load_order(file_paths_reordered)