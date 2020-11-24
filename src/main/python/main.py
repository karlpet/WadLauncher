import sys, os, subprocess

from app.AppContext import *
from PyQt5 import QtWidgets, uic

from app.config import Config
from core.utils.mvcimporter import *

class Ui(QtWidgets.QMainWindow):
    def __init__(self, appctxt):
        super(Ui, self).__init__()

        template_file_path = appctxt.get_resource('template/wadlauncher.ui')
        uic.loadUi(template_file_path, self)

        self.show()

if __name__ == '__main__':
    appctxt = AppContext.Instance()
    config = Config.Instance()
    window = Ui(appctxt)

    models, controllers = mvcimport(os.path.dirname(os.path.abspath(__file__)), window)

    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)