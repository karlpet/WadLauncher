from PyQt5 import uic
from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from app.AppContext import AppContext
from app.helpers.StackedWidgetSelector import add_widget
from app.helpers.ContextMenuFactory import make_context_menu
from app.helpers.WadItemFactory import make_wad_item, DATA_ROLE
from app.views.widgets.promoted.DeselectableTreeView import DeselectableTreeView

template_path = AppContext.Instance().get_resource('template/wadtree.ui')
Form, Base = uic.loadUiType(template_path)

TREE_WAD_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemNeverHasChildren

class WadTreeView(Base, Form):
    def __init__(self, root, models, controller, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        add_widget(root, self, 'WAD_TREE')

        self.wads = models.wads
        self.categories = models.categories
        self.controller = controller

        self.wadtree_model = QStandardItemModel()

        self.moving_item = None
        self.wadtree_model.rowsRemoved.connect(self.row_removed)
        # rowsInserted does NOT work as it is documented to.
        # We use itemChanged signal instead.
        self.wadtree_model.itemChanged.connect(self.text_change_or_row_insert, type=Qt.QueuedConnection)

        self.wadtree = self.findChild(QTreeView, 'wadtree')
        self.wadtree.setDragEnabled(True)
        self.wadtree.viewport().setAcceptDrops(True)
        self.wadtree.setDropIndicatorShown(True)
        self.wadtree.setDragDropMode(QAbstractItemView.InternalMove)
        self.wadtree.setModel(self.wadtree_model)
        self.wadtree.selectionModel().selectionChanged.connect(self.select_tree_index)
        self.wadtree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.wadtree.customContextMenuRequested.connect(self.open_menu)

        self.is_importing = True
        self.appended_wads = []
        root_category = self.categories.find_by(is_root='yes')
        root_item = self.wadtree_model.invisibleRootItem()
        root_item.setData(root_category, DATA_ROLE)
        self.recursive_import(root_item, root_category.get('children', []))
        for wad in self.wads.all():
            if wad['id'] not in self.appended_wads:
                self.wadtree_model.invisibleRootItem().appendRow(self.create_row(wad))
        AppContext.Instance().app.processEvents()
        self.is_importing = False
        self.wadtree.expandAll()

    def text_change_or_row_insert(self, item):
        item_data = item.data()
        item_text = item.text()
        if item_data['model_type'] != 'wads' and item_text != item_data['name']:
            id = item_data['id']
            self.categories.update(id, name=item_text)
            self.categories.save(id)
            return
        dst_parent = self.wadtree_model.invisibleRootItem()
        if item.parent():
            dst_parent = item.parent()
        self.update_parent(dst_parent)

    def row_removed(self, index, *_):
        src_parent = self.wadtree_model.invisibleRootItem()
        if index.isValid():
            src_parent = self.wadtree_model.itemFromIndex(index)
        self.update_parent(src_parent)

    def update_parent(self, parent):
        def get_child(i): return parent.child(i).data()['id']
        children = [get_child(i) for i in range(parent.rowCount())]

        parent_id = parent.data(DATA_ROLE)['id']
        self.categories.update(parent_id, children=children)
        self.categories.save(parent_id)

    def recursive_import(self, parent, children):
        for child_id in children:
            child = None
            try:
                child = self.categories.find(child_id)
            except KeyError:
                try:
                    child = self.wads.find(child_id)
                    self.appended_wads.append(child['id'])
                except KeyError:
                    continue
            child_item = self.create_row(child)
            parent.appendRow(child_item)
            self.recursive_import(child_item, child.get('children', []))

    def open_menu(self, pos):
        index = self.wadtree.indexAt(pos)
        def add_category(): self.add_category(index)
        menu_actions = [('Add Category', add_category)]

        if index.isValid():
            item = self.wadtree_model.itemFromIndex(index)
            item_data = item.data(DATA_ROLE)
            if item_data['model_type'] == 'categories':
                def remove_category():
                    self.remove_category(index)
                remove_category_str = 'Remove category ({})'.format(item_data['name'])
                menu_actions.append((remove_category_str, remove_category))
            elif item_data['model_type'] == 'wads':
                wad_string = item_data.get('title') or item_data.get('name')
                remove_wad_string = 'Remove ({})'.format(wad_string)
                def remove_wad():
                    self.wadtree_model.removeRow(item.row())
                    self.controller.remove_wad(item_data)
                menu_actions.append((remove_wad_string, remove_wad))

        execute_menu = make_context_menu(self, menu_actions)
        execute_menu(pos)

    def add_category(self, index):
        item = None
        try:
            maybe_item = self.wadtree_model.itemFromIndex(index)
            maybe_item_data = maybe_item.data()
            if maybe_item_data['model_type'] == 'categories':
                item = maybe_item
            elif maybe_item_data['model_type'] == 'wads':
                parent_index = index.parent()
                if parent_index.isValid():
                    item = self.wadtree_model.itemFromIndex(parent_index)
                else:
                    item = self.wadtree_model.invisibleRootItem()
        except Exception:
            item = self.wadtree_model.invisibleRootItem()
        child_id = self.categories.create(name='new category', children=[])
        self.categories.save(child_id)
        child_data = self.categories.find(child_id)
        new_child = self.create_row(child_data)
        item.appendRow(new_child)
        # Focus new item:
        AppContext.Instance().app.processEvents()
        new_child_index = self.wadtree_model.indexFromItem(new_child)
        self.wadtree.edit(new_child_index)
    
    def remove_category(self, index):
        if not index.isValid():
            return
        item = self.wadtree_model.itemFromIndex(index)
        parent_item = self.wadtree_model.invisibleRootItem()
        parent_index = index.parent()
        if parent_index.isValid():
            parent_item = self.wadtree_model.itemFromIndex(parent_index)
        for row in range(item.rowCount()):
            child = item.takeChild(row)
            parent_item.appendRow(child)
        item_data = item.data(DATA_ROLE)
        parent_item.removeRow(item.row())
        self.controller.remove_category(item_data)

    def add_wad(self, wad):
        item = self.create_row(wad)
        self.wadtree_model.invisibleRootItem().appendRow(item)

    def remove_wad(self, wad):
        for row in range(self.wadtree_model.rowCount()):
            item = self.wadtree_model.item(row)
            if item and item.data()['id'] == wad['id']:
                self.wadtree_model.removeRow(row)

    def select_tree_index(self, selection):
        if len(selection.indexes()) == 0:
            return
        index = selection.indexes()[0]
        item = self.wadtree_model.itemFromIndex(index)
        if item.data()['model_type'] == 'wads':
            self.wads.select_wad(item.data()['id'])

    def create_row(self, model_item):
        if model_item['model_type'] == 'categories':
            item = QStandardItem(model_item['name'])
            item.setData(model_item, DATA_ROLE)
            nameItemFont = item.font()
            nameItemFont.setBold(True)
            item.setFont(nameItemFont)
            return item
        if model_item['model_type'] == 'wads':
            return make_wad_item(model_item, TREE_WAD_FLAGS)