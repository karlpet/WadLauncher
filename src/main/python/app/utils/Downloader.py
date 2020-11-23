import os, pathlib, urllib

from app.config import Config

MIRRORS = {
    'GERMANY': 'ftp://ftp.fu-berlin.de/pc/games/idgames/',
    'IDAHO': 'ftp://mirrors.syringanetworks.net/idgames/',
    'GREECE': 'ftp://ftp.ntua.gr/pub/vendors/idgames/',
    'GREECE (HTTP)': 'http://ftp.ntua.gr/pub/vendors/idgames/',
    'TEXAS': 'http://ftp.mancubus.net/pub/idgames/',
    'GERMANY (TLS)': 'https://www.quaddicted.com/files/idgames/',
    'NEW YORK': 'http://youfailit.net/pub/idgames/',
    'VIRGINIA': 'http://www.gamers.org/pub/idgames/'
}

def download(search_item, progress_handler=None):
    config = Config.Instance()
    base_path = os.path.expanduser(config['PATHS']['BASE_PATH'])
    temp_dir = os.path.join(base_path, 'temp')
    pathlib.Path(temp_dir).mkdir(parents=True, exist_ok=True)

    mirror_url = MIRRORS['GERMANY']
    dirname = search_item['dir']
    filename = search_item['filename']

    download_url = mirror_url + dirname + filename
    save_path = os.path.join(temp_dir, filename)

    file_path, _ = urllib.request.urlretrieve(download_url, save_path, progress_handler)

    return file_path
