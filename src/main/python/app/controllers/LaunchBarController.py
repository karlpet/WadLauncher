import sys

from app.views.LaunchBarView import LaunchBarView
from app.utils import Launcher

class LaunchBarController:
    def __init__(self):
        pass

    def show(self, root, models):
        self.wads = models.wads
        self.all_iwads = sorted(models.iwads.all(), key=lambda k: k['name'])
        self.all_source_ports = sorted(models.source_ports.all(), key=lambda k: k['name'])
        self.selected_wad = None
        self.selected_iwad = None
        self.selected_source_port = None
        self.view = LaunchBarView(root,
                                  self.all_iwads,
                                  self.all_source_ports,
                                  self.select_iwad,
                                  self.select_source_port,
                                  self.launch_wad_press)

        models.wads.subscribe(self.wads_subscription)

    def wads_subscription(self, data):
        action, data = data

        if action == 'SELECT_WAD':
            self.selected_wad = data
            self.view.update_selected_wad(data)

    def select_iwad(self, index):
        self.selected_iwad = self.all_iwads[index]

    def select_source_port(self, index):
        self.selected_source_port = self.all_source_ports[index]

    def launch_wad_press(self):
        Launcher.launch(
            self.selected_wad,
            self.wads.load_ordered_files,
            self.selected_iwad,
            self.selected_source_port
        )

sys.modules[__name__] = LaunchBarController()