from core.utils.strings import snake_casify, str_filesize

def test_snake_casify():
    assert(snake_casify('CamelCase') == 'camel_case')
    assert(snake_casify('someObject') == 'some_object')
    assert(snake_casify('snake_case') == 'snake_case')

def test_str_filesize():
    assert(str_filesize(123) == '123.00B')
    assert(str_filesize(1024) == '1.00KB')
    assert(str_filesize('1024') == '1.00KB')
    assert(str_filesize(1048576) == '1.00MB')