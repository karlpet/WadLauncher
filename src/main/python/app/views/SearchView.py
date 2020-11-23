from PyQt5 import QtWidgets, QtCore, uic
from app.utils.AppContext import *

search_result_template_path = AppContext.Instance().get_resource('template/search_result_item.ui')
Form, Base = uic.loadUiType(search_result_template_path)

result = [
    { 'author': 'Dale E. Harris', 'size': '4.43 MB', 'date': '06/13/03', 'filename': 'cchest.zip', 'title': 'The Community Chest Project', 'description': 'Following the success of the original Community Chest, Community Chest 2 is a 32 map megawad including levels made by 26 different authors from the Doom Community. Originally announced almost one year ago in December 2003, it is now complete and ready for your enjoyment.' },
    { 'author': 'Dale E. Harris', 'size': '4.43 MB', 'date': '06/13/03', 'filename': 'cchest.zip', 'title': 'The Community Chest Project 2', 'description': 'Following the success of the original Community Chest, Community Chest 2 is a 32 map megawad including levels made by 26 different authors from the Doom Community. Originally announced almost one year ago in December 2003, it is now complete and ready for your enjoyment.' },
    { 'author': 'Dale E. Harris', 'size': '4.43 MB', 'date': '06/13/03', 'filename': 'cchest.zip', 'title': 'The Community Chest Project 3', 'description': 'Following the success of the original Community Chest, Community Chest 2 is a 32 map megawad including levels made by 26 different authors from the Doom Community. Originally announced almost one year ago in December 2003, it is now complete and ready for your enjoyment.' },
    { 'author': 'Dale E. Harris', 'size': '4.43 MB', 'date': '06/13/03', 'filename': 'cchest.zip', 'title': 'The Community Chest Project 4', 'description': 'Following the success of the original Community Chest, Community Chest 2 is a 32 map megawad including levels made by 26 different authors from the Doom Community. Originally announced almost one year ago in December 2003, it is now complete and ready for your enjoyment.' },
]

class SearchResultWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        self.data_labels = ['author', 'size', 'date', 'filename', 'title', 'description']
    
    def set_data(self, **kwargs):
        for key in self.data_labels:
            label = self.findChild(QtWidgets.QLabel, 'search_result_' + key)
            label.setText(kwargs[key])



class SearchView:
    def __init__(self, root):
        self.search_results_container = root.findChild(QtWidgets.QScrollArea, 'search_results_container')
        self.search_results_container.setWidgetResizable(True)
        self.search_results = root.findChild(QtWidgets.QWidget, 'search_results')

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.search_results.setLayout(layout)

        for item in result:
            search_result = SearchResultWidget()
            search_result.set_data(**item)
            layout.addWidget(search_result)

