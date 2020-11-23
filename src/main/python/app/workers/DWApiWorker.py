# Doomworld idgames public api worker wrapper.
# Documentation: https://www.doomworld.com/idgames/api/
import requests, os, enum

from PyQt5.QtCore import QThread, pyqtSignal

SEARCH_TYPES = ['filename', 'title', 'author', 'email', 'description', 'credits', 'editors', 'textfile']
BASE_URL = 'https://www.doomworld.com/idgames/api/api.php?{}&out=json'

class DWApiMethod(enum.Enum):
    IS_ALIVE = 1
    ABOUT = 2
    GET = 3
    SEARCH = 4

class DWApiWorker(QThread):
    error = pyqtSignal(str)
    done = pyqtSignal(object)

    def __init__(self, api_method, *api_args):
        super(DWApiWorker, self).__init__()

        self.api_method = api_method
        self.api_args = api_args

    def run(self):
        m = self.api_method
        result = None
        err = None

        try:
            if m == DWApiMethod.IS_ALIVE:
                result = self.is_alive(*self.api_args)
            elif m == DWApiMethod.ABOUT:
                result = self.about(*self.api_args)
            elif m == DWApiMethod.GET:
                result = self.get(*self.api_args)
            elif m == DWApiMethod.SEARCH:
                result = self.search(*self.api_args)
            else:
                raise Exception('Method not available, available methods: ' + str(list(DWApiMethod)))
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

        if err:
            self.error.emit(str(err))
            return

        self.done.emit(result)

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

    def get(self, filepath):
        _, file = os.path.split(filepath)

        result = self.req('action=get&file={}'.format(file))
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
