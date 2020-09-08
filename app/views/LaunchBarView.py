from PyQt5 import QtWidgets

class LaunchBarView:
    def __init__(self, root,
                 iwads, selected_iwad_index, select_iwad,
                 source_ports, selected_source_port_index, select_source_port):
        self.root = root.findChild(QtWidgets.QWidget, 'LaunchBar')

        self.iwad_selector = self.root.findChild(QtWidgets.QComboBox, 'iWadSelector')
        self.iwad_selector.addItems(iwads)
        self.iwad_selector.setCurrentIndex(selected_iwad_index)
        self.iwad_selector.currentIndexChanged.connect(select_iwad)

        self.source_port_selector = self.root.findChild(QtWidgets.QComboBox, 'sourcePortSelector')
        self.source_port_selector.addItems(source_ports)
        self.source_port_selector.setCurrentIndex(selected_source_port_index)
        self.source_port_selector.currentIndexChanged.connect(select_source_port)
