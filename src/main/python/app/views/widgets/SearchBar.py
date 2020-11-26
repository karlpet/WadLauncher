from PyQt5.QtWidgets import QPushButton, QPushButton, QComboBox, QLineEdit

from app.views.viewmodels.ComboBoxModel import ComboBoxModel
from app.workers.DWApiWorker import SEARCH_TYPES

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
