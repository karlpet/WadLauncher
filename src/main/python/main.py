import sys, os, subprocess

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic

<<<<<<< 9fcb900b9241b0871c7b1824114fba31e30d0d2e
from app.config import Config
from core.utils.mvcimporter import *
=======
from controllers import WadListController, LaunchBarController, MenuBarController
from models import *
from config import Config

>>>>>>> Add initial menubar code.

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

<<<<<<< 9fcb900b9241b0871c7b1824114fba31e30d0d2e
    models, controllers = mvcimport(os.path.dirname(os.path.abspath(__file__)), window)
=======
    wads = Wads()
    iwads = Iwads()
    source_ports = SourcePorts()

    wad_table_controller = WadListController.WadListController(window, wads)
    launch_bar_controller = LaunchBarController.LaunchBarController(window,
                                                                    wads,
                                                                    iwads,
                                                                    source_ports)
    menu_bar_controller = MenuBarController.MenuBarController(window)
>>>>>>> Add initial menubar code.

    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)