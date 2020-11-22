import os, subprocess
from pathlib import Path

from app.config import Config

def launch(wad, iwad, source_port):
    config = Config.Instance()

    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    wad_dir = os.path.join(wads_path, wad['name'])
    wad_file_path = os.path.join(wad_dir, wad['file'])

    wad_save_dir = os.path.join(wad_dir, 'saves')
    Path(wad_save_dir).mkdir(parents=True, exist_ok=True)

    process_call = source_port['template'].format(wad=wad_file_path, iwad=iwad['path'], save_dir=wad_save_dir)

    subprocess.Popen(process_call.split(' '))