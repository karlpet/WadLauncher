from PyQt5 import QtWidgets

class LaunchBarView:
    def __init__(self, layout, layoutWidget):
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.label = QtWidgets.QLabel(layoutWidget)
        self.label.setObjectName("label")
        self.label.setText("No wad selected")
        self.horizontalLayout.addWidget(self.label)
        
        self.comboBox = QtWidgets.QComboBox(layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        
        self.launchWadButton = QtWidgets.QPushButton(layoutWidget)
        self.launchWadButton.setObjectName("launchWadButton")
        self.launchWadButton.setText("Launch")
        self.horizontalLayout.addWidget(self.launchWadButton)
        
        layout.addLayout(self.horizontalLayout)