import os, subprocess
from pathlib import Path

from config import Config

class WadModel:
    def __init__(self):
        self.subscriptions = []

        self.config = Config.Instance()
        wads_path = os.path.expanduser(self.config['PATHS']['WADS_PATH'])

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

    def launch_wad(self, source_port_template, iwad):
        wad = self.get_selected_wad()

        if wad == None: return

        wads_path = os.path.expanduser(self.config['PATHS']['WADS_PATH'])
        wad_dir = os.path.join(wads_path, wad)
        wad_save_dir = os.path.join(wad_dir, 'saves')
        wad_file_path = os.path.join(wad_dir, wad + '.wad')
        iwad_file_path = os.path.expanduser(os.path.join(self.config['PATHS']['IWADS_PATH'], iwad))
        process_call = source_port_template.format(wad=wad_file_path, iwad=iwad_file_path, save_dir=wad_save_dir)

        print(process_call)
        Path(wad_save_dir).mkdir(parents=True, exist_ok=True)
        subprocess.call(process_call.split(' '))