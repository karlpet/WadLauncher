import shutil, os, re, pathlib

from app.config import Config

def unzip(file_path):
    config = Config.Instance()

    wads_path = os.path.expanduser(config['PATHS']['WADS_PATH'])
    
    # remove file extension (.zip or whatever)
    pattern = re.compile(r'\.[a-z0-9]+$')
    file_dir = pattern.sub('', pathlib.Path(file_path).name)

    new_wad_path = os.path.join(wads_path, file_dir)
    pathlib.Path(new_wad_path).mkdir(parents=True, exist_ok=True)

    shutil.unpack_archive(file_path, new_wad_path)

    # need to remove nested directories, if any. We walk the directory.
    tree = [f for f in os.walk(new_wad_path)][0]
    p, directory, files = tree

    if (len(directory) == 1):
        nested_dir = os.path.join(p, directory[0])
        print(nested_dir)
        for file in os.listdir(nested_dir):
            shutil.move(os.path.join(nested_dir, file), os.path.join(new_wad_path, file))
        shutil.rmtree(nested_dir)
    
    return new_wad_path


