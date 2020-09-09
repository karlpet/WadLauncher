#!/usr/bin/python
import sys, os, subprocess

from PyQt5 import QtWidgets, uic

from controllers import WadListController, LaunchBarController
from models import WadModel, IWadModel, SourcePortModel
from config import Config


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./template/wadlauncher.ui', self)

        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    config = Config.Instance()
    window = Ui()

    wad_model = WadModel.WadModel()
    iwad_model = IWadModel.IWadModel()
    source_port_model = SourcePortModel.SourcePortModel()

    wad_table_controller = WadListController.WadListController(window, wad_model)
    launch_bar_controller = LaunchBarController.LaunchBarController(window,
                                                                    wad_model,
                                                                    iwad_model,
                                                                    source_port_model)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
