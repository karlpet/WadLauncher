from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt

def idgames_data_populator(root, item, data_labels, except_elided=['title', 'description']):
    for key in data_labels:
        label = root.findChild(QLabel, 'search_result_' + key)
        text = item.get(key)
        if key == 'size':
            text = str_filesize(text)
        text = text or 'unknown'
        if not (key == 'title' or key == 'description'):
            metrics = QFontMetrics(label.font())
            text = metrics.elidedText(text, Qt.ElideRight, label.width() - 2)
        label.setText(text)


# DETAILVIEW
   def setData(self, item):
        data_labels = ['title', 'filename', 'size', 'date', 'author', 'description', 'credits', 'base', 'buildtime', 'editors', 'bugs','rating']
        for key in data_labels:
            label = self.root.findChild(QtWidgets.QLabel, 'idgames_detail_info_' + key)
            if key == 'size':
                label.setText(str_filesize(item.get(key)))
            else:
                label.setText(str(item.get(key)) or 'unknown')

        self.progressbar = self.root.findChild(QtWidgets.QProgressBar, 'idgames_detail_progress')
        self.progressbar.hide()
        self.download_button = self.root.findChild(QtWidgets.QPushButton, 'idgames_detail_download_button')
        self.download_button.clicked.connect(self.download)
        self.download_button.setEnabled(True)
        self.enabled = True

# SEARCHVIEW
    def setData(self, root, item, controller):
        self.controller = controller

        data_labels = ['author', 'size', 'date', 'filename', 'title', 'description']
        for key in data_labels:
            label = self.findChild(QtWidgets.QLabel, 'search_result_' + key)
            text = item.get(key)
            if key == 'size':
                text = str_filesize(text)
            text = text or 'unknown'
            if not (key == 'title' or key == 'description'):
                metrics = QtGui.QFontMetrics(label.font())
                text = metrics.elidedText(text, QtCore.Qt.ElideRight, label.width() - 2)
            label.setText(text)

        self.id = item.get('id')
        self.progressbar = self.findChild(QtWidgets.QProgressBar, 'search_result_progress')
        self.progressbar.hide()
        self.download_button = self.findChild(QtWidgets.QPushButton, 'search_result_download')
        self.download_button.clicked.connect(self.download)
        self.enabled = True
        self.view_details_button = self.findChild(QtWidgets.QPushButton, 'search_result_details')
        self.view_details_button.clicked.connect(lambda _: self.controller.display_detail(self.id))