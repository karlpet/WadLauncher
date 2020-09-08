import glob, os, functools

from config import Config

class IWadModel:
    def __init__(self):
        config = Config.Instance()

        path = os.path.expanduser(config['PATHS']['IWADS_PATH'])
        files = glob.glob(os.path.join(os.path.abspath(path), '*.wad'))

        self.iwads = []
        for file in files:
            with open(file, 'rb') as fd:
                wad_type = fd.read(4).decode("utf-8")
                if wad_type == 'IWAD':
                    self.iwads.append(os.path.basename(file))
        self.iwads.sort()
        self.selected_iwad_index = -1
        if len(self.iwads) > 0:
            self.selected_iwad_index = 0
        for i in range(len(self.iwads)):
            if self.iwads[i] == 'doom2.wad':
                self.selected_iwad_index = i

    def get_iwads(self):
        return self.iwads

    def get_selected_iwad_index(self):
        return self.selected_iwad_index

    def select_iwad(self, index):
        self.selected_iwad_index = index
