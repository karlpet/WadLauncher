from PyQt5 import QtWidgets, QtGui, QtCore, uic
from app.AppContext import *
from app.workers.DWApiWorker import SEARCH_TYPES
from core.utils.strings import strformat_size, strformat_percentage

search_result_template_path = AppContext.Instance().get_resource('template/search_result_item.ui')
Form, Base = uic.loadUiType(search_result_template_path)

class SearchResultWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

    def setData(self, item, controller):
        self.controller = controller

        data_labels = ['author', 'size', 'date', 'filename', 'title', 'description']
        for key in data_labels:
            label = self.findChild(QtWidgets.QLabel, 'search_result_' + key)
            if key == 'size':
                label.setText(strformat_size(item.get(key)))
            else:
                label.setText(item.get(key) or 'unknown')

        self.id = item.get('id')
        self.downloadButton = self.findChild(QtWidgets.QPushButton, 'search_result_download')
        self.downloadButton.clicked.connect(self.download)
        self.enabled = True

    def download(self):
        self.downloadButton.setEnabled(False)
        if self.enabled:
            self.enabled = False
            self.controller.download(self.id, self.download_progress_handler, self.download_finished_handler)

    def download_progress_handler(self, count, block_size, total_size):
        percentage = strformat_percentage(count * block_size, total_size)
        button_text = 'Downloading... ({})'.format(percentage)
        self.downloadButton.setText(button_text)

    def download_finished_handler(self, _):
        self.downloadButton.setText('Downloaded')

        

class SearchView:
    def __init__(self, root, controller):
        self.searchbar = SearchBar(root, controller)
        self.controller = controller

        self.search_results_container = root.findChild(QtWidgets.QScrollArea, 'search_results_container')
        self.search_results_container.setWidgetResizable(True)
        self.search_results = root.findChild(QtWidgets.QWidget, 'search_results')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(9, 9, 9, 9)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.search_results.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel('Search result will show here...'))

    def updateResults(self, result):
        for i in reversed(range(self.layout.count())): 
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        search_result = result.get('file', [])
        if type(search_result) != list:
            search_result = [search_result]

        warning = result.get('warning', None)
        if warning:
            self.layout.addWidget(QtWidgets.QLabel(warning['type']))
            self.layout.addWidget(QtWidgets.QLabel(warning['message']))

        for item in search_result:
            search_result = SearchResultWidget()
            search_result.setData(item, self.controller)
            self.layout.addWidget(search_result)

class SearchBar:
    def __init__(self, root, controller):
        self.controller = controller

        self.searchbar_search = root.findChild(QtWidgets.QPushButton, 'searchbar_search')
        self.searchbar_type_selector = root.findChild(QtWidgets.QComboBox, 'searchbar_type_selector')
        self.searchbar_input = root.findChild(QtWidgets.QLineEdit, 'searchbar_input')

        self.searchbar_search.clicked.connect(self.search)
        self.searchbar_type_selector.setModel(SearchTypeComboBoxModel(SEARCH_TYPES))
    
    def search(self):
        text = self.searchbar_input.text()

        if (len(text) == 0):
            return

        search_selector_index = self.searchbar_type_selector.currentIndex()
        search_by = SEARCH_TYPES[search_selector_index]
        self.controller.search(text, search_by)

class SearchTypeComboBoxModel(QtCore.QAbstractListModel):
    def __init__(self, search_types = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__search_types = search_types

    def rowCount(self, parent):
        return len(self.__search_types)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__search_types[index.row()]
