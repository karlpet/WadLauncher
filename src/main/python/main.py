import sys, os, subprocess

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic

from controllers import WadListController, LaunchBarController
from models import WadModel, IWadModel, SourcePortModel
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

    wad_model = WadModel.WadModel()
    iwad_model = IWadModel.IWadModel()
    source_port_model = SourcePortModel.SourcePortModel()

    wad_table_controller = WadListController.WadListController(window, wad_model)
    launch_bar_controller = LaunchBarController.LaunchBarController(window,
                                                                    wad_model,
                                                                    iwad_model,
                                                                    source_port_model)

    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)