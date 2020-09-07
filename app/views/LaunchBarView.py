from PyQt5 import QtWidgets

class LaunchBarView:
    def __init__(self, root):
        self.root = root.findChild(QtWidgets.QWidget, 'LaunchBar')