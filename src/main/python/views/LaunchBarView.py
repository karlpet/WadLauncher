from PyQt5 import QtWidgets, QtCore

class SourcePortComboBoxModel(QtCore.QAbstractListModel):
    def __init__(self, source_ports = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__source_ports = source_ports

    def rowCount(self, parent):
        return len(self.__source_ports)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__source_ports[index.row()].get('name')

class IwadComboBoxModel(QtCore.QAbstractListModel):
    def __init__(self, iwads = [], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__iwads = iwads

    def rowCount(self, parent):
        return len(self.__iwads)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__iwads[index.row()].get('name')

class LaunchBarView:
    def __init__(self,
                 root,
                 iwads,
                 source_ports,
                 select_iwad,
                 select_source_port,
                 launch_wad_press):
        root = root.findChild(QtWidgets.QWidget, 'LaunchBar')

        self.selected_wad_name = root.findChild(QtWidgets.QLabel, 'selectedWadName')
        self.selected_wad_name.setText('No wad selected')

        iwad_selector = root.findChild(QtWidgets.QComboBox, 'iWadSelector')
        iwad_selector.setModel(IwadComboBoxModel(iwads))
        iwad_selector.currentIndexChanged.connect(select_iwad)
        iwad_selector.setCurrentIndex(iwad_selector.findText('doom2.wad'))
        select_iwad(iwad_selector.currentIndex())

        source_port_selector = root.findChild(QtWidgets.QComboBox, 'sourcePortSelector')
        source_port_selector.setModel(SourcePortComboBoxModel(source_ports))
        source_port_selector.currentIndexChanged.connect(select_source_port)
        source_port_selector.setCurrentIndex(source_port_selector.findText('gzdoom'))
        select_source_port(source_port_selector.currentIndex())

        launch_wad_button = root.findChild(QtWidgets.QPushButton, 'launchWadButton')
        launch_wad_button.clicked.connect(launch_wad_press)

    def update_selected_wad(self, wad):
        if wad == None:
            self.selected_wad_name.setText('No wad selected')
        else:
            self.selected_wad_name.setText(wad['name'])
