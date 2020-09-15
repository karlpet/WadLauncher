from PyQt5 import QtWidgets

class MenuBarView:
    def __init__(self, root):
        import_zip_action = root.findChild(QtWidgets.QAction, 'actionImport_zip')
        import_zip_action.triggered.connect(lambda: print('import zip triggered'))
