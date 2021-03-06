from PyQt5.QtWidgets import QLabel, QProgressBar, QPushButton
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt

from core.utils.strings import str_filesize

class IdgamesResponseWidget:
    def __init__(self, root, data_labels, object_name_scope, download_start_callback, except_elided=['title', 'description']):
        self.root = root
        self.data_labels = data_labels
        self.object_name_scope = object_name_scope + '_'
        self.except_elided = except_elided
        self.download_start_callback = download_start_callback
        self.id = None

    def set_data(self, item, already_downloaded):
        for key in self.data_labels:
            label = self.root.findChild(QLabel, self.object_name_scope + key)
            text = str(item.get(key))
            if key == 'size':
                text = str_filesize(text)
            text = text or 'unknown'
            if key not in self.except_elided:
                metrics = QFontMetrics(label.font())
                text = metrics.elidedText(text, Qt.ElideRight, label.width() - 2)
            label.setText(text)

        self.id = item.get('id')
        self.progressbar = self.root.findChild(QProgressBar, self.object_name_scope + 'progress')
        self.progressbar.hide()
        self.download_button = self.root.findChild(QPushButton, self.object_name_scope + 'download')
        self.download_button.clicked.connect(self.download)
        self.download_button.setText('Download')

        self.enabled = not already_downloaded
        self.download_button.setEnabled(not already_downloaded)
        if already_downloaded:
            self.download_finished()

    def download(self):
        self.download_button.setEnabled(False)
        if self.enabled:
            self.progressbar.setValue(0)
            self.download_button.setText('Downloading...')
            self.enabled = False
            self.download_start_callback(self.id)

    def download_progress(self, count, block_size, total_size):
        self.download_button.setEnabled(False)
        percentage = min((count * block_size) / total_size * 100, 100)
        self.progressbar.setValue(percentage)
        self.progressbar.show()

    def download_finished(self):
        self.download_button.setEnabled(False)
        self.download_button.setText('Downloaded')
        self.progressbar.hide()
