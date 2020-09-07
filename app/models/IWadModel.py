import glob, os

from config import Config

class IWadModel:
    def __init__(self):
        config = Config.Instance()

        path = os.path.expanduser(config['PATHS']['IWADS_PATH'])
        files = glob.glob(os.path.join(os.path.abspath(path), '*.wad'))

        print(files)

        self.i_wads = []

        for file in files:
            with open(file, 'rb') as fd:
                wad_type = fd.read(4).decode("utf-8") 
                if wad_type == 'IWAD':
                    self.i_wads.append(file)

        print(self.i_wads)
