from PyQt5 import QtWidgets

class LaunchBarView:
    def __init__(self, root, iwads, selected_iwad_index, select_iwad):
        self.root = root.findChild(QtWidgets.QWidget, 'LaunchBar')

        self.iwad_selector = self.root.findChild(QtWidgets.QComboBox, 'iWadSelector')
        self.iwad_selector.addItems(iwads)
        self.iwad_selector.setCurrentIndex(selected_iwad_index)
        self.iwad_selector.currentIndexChanged.connect(select_iwad)
