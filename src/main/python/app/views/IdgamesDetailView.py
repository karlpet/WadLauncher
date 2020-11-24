from PyQt5 import QtWidgets

from core.utils.strings import strformat_size

class IdgamesDetailView():
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        root.findChild(QtWidgets.QStackedWidget, 'MainContentStack').currentChanged.connect(self.controller.get_data)
        
        self.mirror_button_group = QtWidgets.QButtonGroup()
        button_layout = self.root.findChild(QtWidgets.QVBoxLayout, 'idgames_detail_download_layout')
        radio_button_labels = ['Germany','Idaho','Greece','Greece (HTTP)','Texas','Germany (TLS)','New York','Virginia']
        for i, label in enumerate(radio_button_labels):
            radio_button = QtWidgets.QRadioButton(label)
            radio_button.setObjectName(label.upper())
            radio_button.setChecked(i == 0)
            button_layout.addWidget(radio_button)
            self.mirror_button_group.addButton(radio_button)

    def setData(self, item):
        data_labels = ['title', 'filename', 'size', 'date', 'author', 'description', 'credits', 'base', 'buildtime', 'editors', 'bugs','rating']
        for key in data_labels:
            label = self.root.findChild(QtWidgets.QLabel, 'idgames_detail_info_' + key)
            if key == 'size':
                label.setText(strformat_size(item.get(key)))
            else:
                label.setText(str(item.get(key)) or 'unknown')

        self.progressbar = self.root.findChild(QtWidgets.QProgressBar, 'idgames_detail_progress')
        self.progressbar.hide()
        self.downloadButton = self.root.findChild(QtWidgets.QPushButton, 'idgames_detail_download_button')
        self.downloadButton.clicked.connect(self.download)
        self.downloadButton.setEnabled(True)
        self.enabled = True

    def download(self):
        self.downloadButton.setEnabled(False)

        if self.enabled:
            mirror = self.mirror_button_group.checkedButton().objectName()
            self.progressbar.show()
            self.progressbar.setValue(0)
            self.downloadButton.setText('Downloading...')
            self.enabled = False
            self.controller.download(mirror, self.download_progress_handler, self.download_finished_handler)

    def download_progress_handler(self, count, block_size, total_size):
        percentage = min((count * block_size) / total_size * 100, 100)
        self.progressbar.setValue(percentage)
        

    def download_finished_handler(self, _):
        self.downloadButton.setText('Downloaded')
        self.progressbar.hide()
