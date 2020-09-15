import sys, os, subprocess

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic

from controllers import WadListController, LaunchBarController
from models import *
from config import Config


class Ui(QtWidgets.QMainWindow):
    def __init__(self, appctxt):
        super(Ui, self).__init__()

        template_file_path = appctxt.get_resource('template/wadlauncher.ui')
        uic.loadUi(template_file_path, self)

        self.show()

if __name__ == '__main__':
    appctxt = ApplicationContext()
    config = Config.Instance()
    window = Ui(appctxt)

    wads = Wads()
    iwads = Iwads()
    source_ports = SourcePorts()

    wad_table_controller = WadListController.WadListController(window, wads)
    launch_bar_controller = LaunchBarController.LaunchBarController(window,
                                                                    wads,
                                                                    iwads,
                                                                    source_ports)

    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)