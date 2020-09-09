from PyQt5 import QtWidgets

class LaunchBarView:
    def __init__(self,
                 root,
                 iwads,
                 selected_iwad_index,
                 select_iwad,
                 source_ports,
                 selected_source_port_index,
                 select_source_port,
                 launch_wad_press):
        self.root = root.findChild(QtWidgets.QWidget, 'LaunchBar')

        self.selected_wad_name = self.root.findChild(QtWidgets.QLabel, 'selectedWadName')
        self.selected_wad_name.setText('No wad selected')

        self.iwad_selector = self.root.findChild(QtWidgets.QComboBox, 'iWadSelector')
        self.iwad_selector.addItems(iwads)
        self.iwad_selector.setCurrentIndex(selected_iwad_index)
        self.iwad_selector.currentIndexChanged.connect(select_iwad)

        self.source_port_selector = self.root.findChild(QtWidgets.QComboBox, 'sourcePortSelector')
        self.source_port_selector.addItems(source_ports)
        self.source_port_selector.setCurrentIndex(selected_source_port_index)
        self.source_port_selector.currentIndexChanged.connect(select_source_port)

        self.launch_wad_button = self.root.findChild(QtWidgets.QPushButton, 'launchWadButton')
        self.launch_wad_button.clicked.connect(launch_wad_press)

    def update_selected_wad_name(self, wad):
        if wad == None:
            self.selected_wad_name.setText('No wad selected')
        else:
            self.selected_wad_name.setText(wad)
