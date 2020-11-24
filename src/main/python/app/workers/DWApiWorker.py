# Doomworld idgames public api worker wrapper.
# Documentation: https://www.doomworld.com/idgames/api/
import requests, os, enum

from PyQt5.QtCore import QThread, pyqtSignal

SEARCH_TYPES = ['filename', 'title', 'author', 'email', 'description', 'credits', 'editors', 'textfile']
BASE_URL = 'https://www.doomworld.com/idgames/api/api.php?{}&out=json'

class DWApiMethod(enum.Enum):
    IS_ALIVE = 1
    SEARCH = 2
    ABOUT = 3
    GET = 4

class DWApiWorker(QThread):
    done = pyqtSignal(object)

    def __init__(self, api_method, *api_args):
        super(DWApiWorker, self).__init__()

        api_calls = dict((data, getattr(self, data.name.lower())) for data in DWApiMethod)

        self.api_call = api_calls[api_method]
        self.api_args = api_args

    def run(self):
        result = None
        err = None

        try:
            result = self.api_call(*self.api_args)
        except Exception as e:
            err = e
        except requests.exceptions.HTTPError as e:
            err = e
        except requests.exceptions.ConnectionError as e:
            err = e
        except requests.exceptions.Timeout as e:
            err = e
        except requests.exceptions.RequestException as e:
            err = e

        self.done.emit((result, err))

    def req(self, query):
        response = requests.get(BASE_URL.format(query))
        response.raise_for_status()

        result = response.json()
        content = result.get('content', False)
        if content:
            result.pop('content')
            return {**content, **result}

        return result

    def is_alive(self):
        result = self.req('action=ping')
        return result['status'] == 'true'

    def about(self):
        result = self.req('action=about')
        return result

    def get(self, filename, get_type):
        result = self.req('action=get&{type}={file}'.format(type=get_type, file=filename))
        error = result.get('error', False)

        if error:
            raise Exception(error)

        return result

    def search(self, query, search_by='filename'):
        # search query demands at least 3 chars, and uses '_' as an 'any' type char
        # 'gd'.ljust(3, '_') -> 'gd_'
        # 'doom'.ljust(3, '_') -> 'doom'
        query = query.ljust(3, '_')

        result = self.req('action=search&query={}&type={}'.format(query, search_by))
        error = result.get('error', False)

        if error:
            raise Exception(error)

        return result
