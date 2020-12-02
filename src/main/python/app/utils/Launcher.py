import os, subprocess
from pathlib import Path

from app.config import Config

def launch(wad, iwad, source_port):
    config = Config.Instance()

    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    wad_dir = os.path.join(wads_path, wad['name'])

    wad_save_dir = os.path.join(wad_dir, 'saves')
    Path(wad_save_dir).mkdir(parents=True, exist_ok=True)

    executable_path = os.path.join(source_port['dir'], source_port['executable'])
    files = ' '.join(wad['file_paths'])

    process_call = [
        executable_path,
        source_port['wad_arg'],
        files,
        source_port['iwad_arg'],
        iwad['path'],
        source_port['save_arg'],
        wad_save_dir,
    ]

    subprocess.Popen(process_call, cwd=source_port['dir'])