#!/usr/bin/python
import sys, os, subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex

from controllers import MainWindowController, WadTableController, LaunchBarController
from config import config

def main():
    app = QApplication(sys.argv)
    main_window_controller = MainWindowController.MainWindowController()
    wad_table_controller = WadTableController.WadTableController(main_window_controller.view)
    launch_bar_controller = LaunchBarController.LaunchBarController(main_window_controller.view)

    main_window_controller.view.mainWindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# class MainView:
#     def __init__(self, list_view_model, on_launch_press, on_selection_change):
#         self.selected_wad = None
#         self.q_main_window = QMainWindow()

#         main_window = WadLauncher.Ui_MainWindow()
#         main_window.setupUi(self.q_main_window)
#         main_window.pushButton.clicked.connect(on_launch_press)
#         main_window.listView.setModel(list_view_model)
#         main_window.listView.clicked[QModelIndex].connect(on_selection_change)


#     def render(self):
#         self.q_main_window.show()

# class MainController:
#     def __init__(self, model):
#         self.model = model
#         self.view = MainView(self.model.list_view_model,
#                              self.on_launch_press,
#                              self.on_selection_change)
#         self.view.render()

#     def on_launch_press(self):
#         self.model.launch_wad()

#     def on_selection_change(self, index):
#         self.model.select_wad(index.row())
    

# class MainModel:
#     def __init__(self):
#         self.path = config['WADS']['WADS_PATH']

#         self.subscriptions = []
#         self.wad_list = [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
#         self.selected_wad = self.wad_list[0]
#         self.list_view_model = QStandardItemModel()

#         for wad in self.wad_list:
#             item = QStandardItem(wad)
#             self.list_view_model.appendRow(item)

#     def select_wad(self, index):
#         self.selected_wad = self.wad_list[index]

#     def launch_wad(self):
#         wad_base_path = os.path.join(self.path, self.selected_wad)
#         wad_path = wad_base_path + '/' + self.selected_wad + '.wad'

#         subprocess.call(['gzdoom', wad_path])
