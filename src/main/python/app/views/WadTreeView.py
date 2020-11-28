from PyQt5 import uic
from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from collections import deque

from app.AppContext import AppContext
from app.helpers.StackedWidgetSelector import add_widget
from app.helpers.ContextMenuFactory import make_context_menu
from app.views.widgets.promoted.DeselectableTreeView import DeselectableTreeView

template_path = AppContext.Instance().get_resource('template/wadtree.ui')
Form, Base = uic.loadUiType(template_path)

DATA_ROLE = Qt.UserRole + 1

class WadTreeView(Base, Form):
    def __init__(self, root, models, controller, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        add_widget(root, self, 'WAD_TREE')

        self.wads = models.wads
        self.categories = models.categories
        self.controller = controller

        self.wadtree_model = QStandardItemModel()
        self.wadtree_model.itemChanged.connect(self.internal_move)
        self.selected_index = None

        self.wadtree = self.findChild(DeselectableTreeView, 'wadtree')
        self.wadtree.setDragEnabled(True)
        self.wadtree.viewport().setAcceptDrops(True)
        self.wadtree.setDropIndicatorShown(True)
        self.wadtree.setDragDropMode(QAbstractItemView.InternalMove)
        self.wadtree.setModel(self.wadtree_model)
        self.wadtree.selectionModel().selectionChanged.connect(self.select_tree_index)
        self.wadtree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.wadtree.customContextMenuRequested.connect(self.open_menu)
        
        self.importData(self.categories.all() + self.wads.all())
        self.wadtree.expandAll()

    def internal_move(self, item):
        model_item = item.data(DATA_ROLE)
        id = model_item['id']
        model_type = model_item['model_type']

        display_name = item.data(Qt.DisplayRole)
        if model_type == 'categories' and model_item['name'] != display_name:
            self.categories.update(id, name=display_name)
            self.categories.save(id)
            return

        new_category_id = None
        index = item.index()
        parent_index = index.parent()

        if parent_index.isValid():
            parent = self.wadtree_model.itemFromIndex(parent_index)
            new_category_id = parent.data(DATA_ROLE)['id']
        
        if new_category_id != model_item.get('category_id'):
            model = getattr(self, model_type)
            model.update(id, category_id=new_category_id)
            model.save(id)

    def open_menu(self, pos):
        menu_actions = { 'add Category': self.add_category }
        index = self.selected_index

        if index != None:
            item = self.wadtree_model.itemFromIndex(index)
            item_data = item.data(DATA_ROLE)
            if item_data['model_type'] == 'categories':
                def remove_action(): self.remove_category(item)
                menu_actions['Remove category (' + item_data['name'] + ')'] = remove_action

        execute_menu = make_context_menu(self, menu_actions)
        execute_menu(pos)

    def add_category(self):
        id = self.categories.create(name='new category', category_id=None)

        parent = None
        if self.selected_index != None:
            item = self.wadtree_model.itemFromIndex(self.selected_index)
            item_data = item.data(DATA_ROLE)
            if item_data['model_type'] == 'categories':
                parent = item
            else:
                parent_index = self.selected_index.parent()
                if parent_index.isValid():
                    parent = self.wadtree_model.itemFromIndex(parent_index)
        if parent:
            parent_data = parent.data(DATA_ROLE)
            self.categories.update(id, category_id=parent_data['id'])
        else:
            parent = self.wadtree_model.invisibleRootItem()
        
        item = self.create_row(self.categories.find(id))
        parent.appendRow(item)
        self.categories.save(id)
    
    def remove_category(self, item):
        index = item.index()
        parent_item = self.wadtree_model.invisibleRootItem()
        parent_index = index.parent()
        parent_id = None
        if parent_index.isValid():
            parent_item = self.wadtree_model.itemFromIndex(parent_index)
            parent_id = parent_item.data(DATA_ROLE)['id']
        children = []
        for row in range(item.rowCount()):
            child = item.takeChild(row)
            parent_item.appendRow(child)
            children.append(child.data(DATA_ROLE))

        item_data = item.data(DATA_ROLE)
        self.controller.remove_category(item_data, children)
        parent_item.removeRow(item.row())

    def add_wad(self, wad):
        item = self.create_row(wad)
        self.wadtree_model.invisibleRootItem().appendRow(item)

    def remove_wad(self, wad):
        for row in range(self.wadtree_model.rowCount()):
            item = self.wadtree_model.item(row)
            if item.data(DATA_ROLE)['id'] == wad['id']:
                self.wadtree_model.removeRow(row)


    def select_tree_index(self, selection):
        if len(selection.indexes()) == 0:
            self.selected_index = None
            return
        self.selected_index = selection.indexes()[0]
        parent = self.selected_index.parent()

        selected_data = self.get_data_from_index(self.selected_index)
        if selected_data['model_type'] == 'wads':
            self.wads.select_wad(selected_data['id'])
    
    def get_data_from_index(self, index):
        item = index.model().itemFromIndex(index)

        return item.data(DATA_ROLE)

    def importData(self, data, root=None):
        self.wadtree_model.setRowCount(0)
        if root is None:
            root = self.wadtree_model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value.get('category_id') == None:
                parent = root
            else:
                pid = value.get('category_id')
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]

            id = value['id']
            item = self.create_row(value)
            parent.appendRow(item)
            seen[id] = parent.child(parent.rowCount() - 1)
        
    def create_row(self, model_item):
        item = QStandardItem(model_item['name'])
        item.setData(model_item, DATA_ROLE)
        if model_item['model_type'] == 'categories':
            nameItemFont = item.font()
            nameItemFont.setBold(True)
            item.setFont(nameItemFont)
        if model_item['model_type'] == 'wads':
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemNeverHasChildren
            item.setFlags(flags)
        return item