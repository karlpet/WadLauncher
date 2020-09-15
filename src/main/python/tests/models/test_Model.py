from unittest import mock, TestCase
import json

from models.Model import Model

case = TestCase()

# ----- MOCK DATA -----
mock_data = {
    '0': {'id': '0', 'name': 'going down', 'file': 'gd.wad'},
    '1': {'id': '1', 'name': 'miasma', 'file': 'miasma.wad'},
    '2': {'id': '2', 'name': 'sunder', 'file': 'sunder.wad'},
}

def mock_loader():
    return mock_data.values()

def mock_saver(data):
    return json.dumps(data)


# ----- TEST CASES -----
def test_intance_creation():
    mock_model = Model()

def test_loader():
    mock_model = Model(loader=mock_loader)
    mock_model.load()

    case.assertCountEqual(mock_model.all(), mock_data.values())

def test_saver():
    mock_model = Model(loader=mock_loader, saver=mock_saver)

    assert(mock_model.save() == '{}')

    mock_model.load()
    json_string = mock_model.save()

    case.assertDictEqual(json.loads(json_string), mock_data)

def test_create():
    mock_model = Model(loader=mock_loader, saver=mock_saver)
    mock_model.load()
    wad = {'name':'foo', 'file':'foo.wad'}

    id = mock_model.create(**wad)
    assert(mock_model.find(id).items() >= wad.items())

def test_find():
    mock_model = Model(loader=mock_loader)
    mock_model.load()

    case.assertDictEqual(mock_model.find('0'), mock_data.get('0'))

def test_find_by():
    mock_model = Model(loader=mock_loader)
    mock_model.load()

    # Finding by one attribute
    case.assertDictEqual(mock_model.find_by(name='going down'), mock_data.get('0'))

    # Finding by multiple attributes
    case.assertDictEqual(mock_model.find_by(name='miasma', file='miasma.wad'), mock_data.get('1'))

    # Returns None if not found
    assert(mock_model.find_by(name='should not be found', file='miasma.wad') == None)

def test_update():
    mock_model = Model(loader=mock_loader, saver=mock_saver)
    mock_model.load()

    mock_model.update('2', file='sunder2.wad')
    assert(mock_model.find('2').get('file') == 'sunder2.wad')
    # other attributes should be the same
    assert(mock_model.find_by(id='2', name='sunder', file='sunder2.wad') != None)

    # throw error when trying to update item that doesnt exist
    def should_throw_key_error():
        mock_model.update('3', name='key error should be thrown')

    case.assertRaises(KeyError, should_throw_key_error)

def test_delete():
    mock_model = Model(loader=mock_loader, saver=mock_saver)
    mock_model.load()

    deleted = mock_model.delete('2')
    case.assertDictEqual(deleted, mock_data.get('2'))

    def should_throw_key_error():
        mock_model.find('2')
    case.assertRaises(KeyError, should_throw_key_error)

def test_subscribe():
    mock_model = Model(loader=mock_loader)
    mock_func1 = mock.MagicMock()
    mock_func2 = mock.MagicMock()

    unsubscribe = mock_model.subscribe(mock_func1)
    mock_model.subscribe(mock_func2)

    mock_model.broadcast('data')
    mock_func1.assert_called_with('data')
    mock_func2.assert_called_with('data')

    # if unsubscribed, mock_func1 should not be called again
    unsubscribe()
    # mock_func2 should still function as usual
    mock_func2.reset_mock()
    mock_model.broadcast('data')
    mock_func1.assert_called_once_with('data')
    mock_func2.assert_called_with('data')

    
