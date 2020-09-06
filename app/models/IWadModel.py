#from config import config
import glob
import os

class IWadModel:
    def __init__(self):
        path = os.path.expanduser('~/.config/gzdoom')
        files = glob.glob(os.path.join(os.path.abspath(path), '*.wad'))

        print(files)

        self.i_wads = []

        for file in files:
            with open(file, 'rb') as fd:
                wad_type = fd.read(4).decode("utf-8") 
                if wad_type == 'IWAD':
                    self.i_wads.append(file)

        print(self.i_wads)

IWadModel()