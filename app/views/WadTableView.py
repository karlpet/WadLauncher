from PyQt5 import QtWidgets

class WadTableView:
    def __init__(self, layout, layoutWidget):
        self.wadTableView = QtWidgets.QTableView(layoutWidget)
        self.wadTableView.setObjectName("wadTableView")
        layout.addWidget(self.wadTableView)
