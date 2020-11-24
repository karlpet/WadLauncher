from PyQt5 import QtWidgets
from core.utils.strings import strformat_size

class IdgamesDetailView():
    def __init__(self, root, controller):
        """idgames_detail_download_mirror_select"""
        self.controller = controller
        self.root = root
        root.findChild(QtWidgets.QStackedWidget, 'MainContentStack').currentChanged.connect(self.controller.get_data)

    def setData(self, item):
        data_labels = ['title', 'filename', 'size', 'date', 'author', 'description', 'credits', 'base', 'buildtime', 'editors', 'bugs','rating']
        for key in data_labels:
            label = self.root.findChild(QtWidgets.QLabel, 'idgames_detail_info_' + key)
            if key == 'size':
                label.setText(strformat_size(item.get(key)))
            else:
                label.setText(str(item.get(key)) or 'unknown')

        self.id = item.get('id')
        self.progressbar = self.root.findChild(QtWidgets.QProgressBar, 'idgames_detail_progress')
        self.progressbar.hide()
        self.downloadButton = self.root.findChild(QtWidgets.QPushButton, 'idgames_detail_download_button')
        self.downloadButton.clicked.connect(self.download)
        self.enabled = True

    def download(self):
        self.downloadButton.setEnabled(False)
        if self.enabled:
            self.progressbar.show()
            self.progressbar.setValue(0)
            self.downloadButton.setText('Downloading...')
            self.enabled = False
            self.controller.download(self.id, self.download_progress_handler, self.download_finished_handler)

    def download_progress_handler(self, count, block_size, total_size):
        percentage = min((count * block_size) / total_size * 100, 100)
        self.progressbar.setValue(percentage)
        

    def download_finished_handler(self, _):
        self.downloadButton.setText('Downloaded')
        self.progressbar.hide()
