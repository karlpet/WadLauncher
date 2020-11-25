from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt

from app.views.viewmodels.ComboBoxModel import *
from app.AppContext import *
from app.workers.DWApiWorker import SEARCH_TYPES
from app.views.widgets.IdgamesResponseWidget import *

from core.utils.strings import str_filesize

search_result_template_path = AppContext.Instance().get_resource('template/search_result_item.ui')
Form, Base = uic.loadUiType(search_result_template_path)

class SearchResultWidget(Base, Form):
    def __init__(self, controller, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        self.controller = controller

        data_labels = ['author', 'size', 'date', 'filename', 'title', 'description']
        self.idgames_response_widget = IdgamesResponseWidget(self, data_labels, 'search_result', self.controller.download)

    def set_data(self, item):
        self.idgames_response_widget.set_data(item)

        self.view_details_button = self.findChild(QPushButton, 'search_result_details')
        self.view_details_button.clicked.connect(lambda _: self.controller.display_detail(item['id']))

class IdgamesSearchView:
    def __init__(self, root, controller):
        self.searchbar = SearchBar(root, controller)
        self.controller = controller
        self.root = root

        self.search_results_container = root.findChild(QScrollArea, 'idgames_search_results_container')
        self.search_results_container.setWidgetResizable(True)
        self.search_results = root.findChild(QWidget, 'idgames_search_results')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(9, 9, 9, 9)
        self.layout.setAlignment(Qt.AlignTop)
        self.search_results.setLayout(self.layout)

        self.layout.addWidget(QLabel('Search result will show here...'))

    def updateResults(self, result):
        for i in reversed(range(self.layout.count())): 
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            if widgetToRemove != None:
                widgetToRemove.setParent(None)

        search_result = result[0].get('file', [])
        if type(search_result) != list:
            search_result = [search_result]

        warning = result[0].get('warning', None)
        if warning:
            self.layout.addWidget(QLabel(warning['type']))
            self.layout.addWidget(QLabel(warning['message']))

        for item in search_result:
            search_result_widget = SearchResultWidget(self.controller)
            search_result_widget.set_data(item)
            self.layout.addWidget(search_result_widget)
        
        self.layout.addStretch()

class SearchBar:
    def __init__(self, root, controller):
        self.controller = controller

        self.searchbar_search = root.findChild(QPushButton, 'idgames_searchbar_search')
        self.searchbar_type_selector = root.findChild(QComboBox, 'idgames_searchbar_type_selector')
        self.searchbar_input = root.findChild(QLineEdit, 'idgames_searchbar_input')

        self.searchbar_search.clicked.connect(self.search)
        self.searchbar_type_selector.setModel(ComboBoxModel(SEARCH_TYPES))

    def search(self):
        text = self.searchbar_input.text()

        if (len(text) == 0):
            return

        search_selector_index = self.searchbar_type_selector.currentIndex()
        search_by = SEARCH_TYPES[search_selector_index]
        self.controller.search(text, search_by)
