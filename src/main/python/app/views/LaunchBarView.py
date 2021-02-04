import os

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton
from app.views.viewmodels.ComboBoxModel import *

class LaunchBarView:
    def __init__(self,
                 root,
                 iwads,
                 source_ports,
                 select_iwad,
                 select_source_port,
                 launch_wad_press):
        root = root.findChild(QWidget, 'launchbar')

        self.selected_wad_name = root.findChild(QLabel, 'launchbar_selected_wad')
        self.selected_wad_name.setText('No wad selected')

        iwad_selector = root.findChild(QComboBox, 'launchbar_iwad_selector')
        iwad_selector.setModel(ComboBoxModel(iwads, 'name'))
        iwad_selector.currentIndexChanged.connect(select_iwad)
        iwad_selector.setCurrentIndex(iwad_selector.findText('doom2.wad'))
        select_iwad(iwad_selector.currentIndex())

        source_port_selector = root.findChild(QComboBox, 'launchbar_source_port_selector')
        source_port_selector.setModel(ComboBoxModel(source_ports, 'name'))
        source_port_selector.currentIndexChanged.connect(select_source_port)
        source_port_selector.setCurrentIndex(source_port_selector.findText('gzdoom'))
        select_source_port(source_port_selector.currentIndex())

        launch_wad_button = root.findChild(QPushButton, 'launchbar_launch_button')
        launch_wad_button.clicked.connect(launch_wad_press)

    def update_selected_wad(self, wad):
        if wad == None:
            self.selected_wad_name.setText('No wad selected')
        else:
            self.selected_wad_name.setText((wad.get('title') or wad['name']) + ' ({})'.format(os.path.basename(wad['file_path'])))
