from PyQt5.QtWidgets import QAction, QFileDialog, QDialog

class MenuBarView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.import_zip_action = root.findChild(QAction, 'action_file_import_zip')
        self.import_zip_action.triggered.connect(self.file_dialog_opener)

    def file_dialog_opener(self):
        dialog = QFileDialog(self.root, 'Select zip file to import')
        if dialog.exec_() == QDialog.Accepted:
            self.controller.select_unzip_file(dialog.selectedFiles()[0])