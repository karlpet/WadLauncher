from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton

from app.AppContext import *
from app.views.widgets.IdgamesResponseWidget import *

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
        already_downloaded = bool(self.controller.wads.find_by(id=item['id']))
        self.idgames_response_widget.set_data(item, already_downloaded)

        self.view_details_button = self.findChild(QPushButton, 'search_result_details')

        def display_wad(): self.controller.display_detail(item['id'])
        self.view_details_button.clicked.connect(display_wad)
