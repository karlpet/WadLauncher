import os

from config import Config

class WadModel:
    def __init__(self):
        self.subscriptions = []

        config = Config.Instance()
        wads_path = config['PATHS']['WADS_PATH']

        self.wads = [dir for dir in os.listdir(wads_path)
                         if os.path.isdir(os.path.join(wads_path, dir))]
        self.selected_wad_index = -1
    
    def get_wads(self):
        return self.wads
    
    def get_selected_wad(self):
        if self.selected_wad_index == -1:
            return None
        else:
            return self.wads[self.selected_wad_index]
    
    def select_wad(self, index):
        self.selected_wad_index = index

        self.broadcast(('SELECT_WAD', self.get_selected_wad()))

    def subscribe(self, func):
        self.subscriptions.append(func)

    def broadcast(self, data):
        for subscription in self.subscriptions:
            subscription(data)