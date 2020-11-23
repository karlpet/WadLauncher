# Doomworld idgames public api wrapper.
# Documentation: https://www.doomworld.com/idgames/api/
import requests
import os

base_url = 'https://www.doomworld.com/idgames/api/api.php?{}&out=json'

def req(query):
    response = requests.get(base_url.format(query))
    response.raise_for_status()

    result = response.json()
    content = result.get('content', False)
    if content:
        return content

    return result

def is_alive():
    result = req('action=ping')
    return result['status'] == 'true'

def about():
    result = req('action=about')
    return result

def get(filepath):
    _, file = os.path.split(filepath)

    result = req('action=get&file={}'.format(file))
    error = result.get('error', False)

    if error:
        raise Exception(error)

    return result

SEARCH_TYPES = ['filename', 'title', 'author', 'email', 'description', 'credits', 'editors', 'textfile']
def search(query, search_by='filename'):
    # search query demands at least 3 chars, and uses '_' as an 'any' type char
    # 'gd'.ljust(3, '_') -> 'gd_'
    # 'doom'.ljust(3, '_') -> 'doom'
    query = query.ljust(3, '_')

    result = req('action=search&query={}&type={}'.format(query, search_by))
    error = result.get('error', False)

    if error:
        raise Exception(error)

    return result
