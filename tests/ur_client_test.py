# -*- coding: utf-8 -*-

import asyncio
from unittest.mock import Mock

import pytest
from pytest_mock import mocker
from urchintai_client.ur_client import UrClient

ignored_request_sender = None

@pytest.mark.asyncio
async def test_should_throw_error_if_no_property_argument():
    '''
    Either url or property_code is required
    '''

    # Arrange
    client = UrClient(ignored_request_sender)

    # Act
    with pytest.raises(ValueError) as e:
        await client.is_property_vacant()

    # Assert
    assert str(e.value) == 'Please provide either property\'s URL or property code'

@pytest.mark.asyncio
async def test_should_return_true_if_property_vacant_using_url():
    '''
    If the list of empty room returned from UR Chintai API is not "null",
    that property is vacant.
    '''

    # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html'

    request_sender = setup_request_sender('not null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_property_vacant(url=url)

    # Assert
    assert isVacant == True

@pytest.mark.asyncio
async def test_should_return_true_if_property_vacant_using_code():
    '''
    If the list of empty room returned from UR Chintai API is not "null",
    that property is vacant.
    '''

    # Arrange
    property_code = {
        'store_code': '40',
        'house_code': '412',
        'type': '0'
    }

    request_sender = setup_request_sender('not null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_property_vacant(property_code=property_code)

    # Assert
    assert isVacant == True

@pytest.mark.asyncio
async def test_should_return_false_if_property_full_using_url():
    '''
    If the list of empty room returned from UR Chintai API is "null",
    that property is full.
    '''

    # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html'

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_property_vacant(url=url)

    # Assert
    assert isVacant == False

@pytest.mark.asyncio
async def test_should_return_false_if_property_full_using_code():
    '''
    If the list of empty room returned from UR Chintai API is "null",
    that property is full.
    '''

    # Arrange
    property_code = {
        'store_code': '40',
        'house_code': '412',
        'type': '0'
    }

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    is_vacant = await client.is_property_vacant(property_code=property_code)

    # Assert
    assert is_vacant == False

@pytest.mark.asyncio
async def test_should_prioritize_property_code_over_url(mocker):
    '''
    If both room code and URL are provided, use room code.
    '''

     # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html'
    property_code = {
        'store_code': '40',
        'house_code': '412',
        'type': '0'
    }

    mock_parser = mocker.patch('urchintai_client.ur_parser.get_property_code_from_url', \
        return_value=property_code)

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    await client.is_property_vacant(url=url, property_code=property_code)

    # Assert
    mock_parser.assert_not_called()

@pytest.mark.asyncio
async def test_should_throw_error_if_no_room_argument():
    '''
    Either url or room_code is required
    '''

    # Arrange
    client = UrClient(ignored_request_sender)

    # Act
    with pytest.raises(ValueError) as e:
        await client.is_room_vacant()

    # Assert
    assert str(e.value) == 'Please provide either room\'s URL or room code'

@pytest.mark.asyncio
async def test_should_return_true_if_room_vacant_using_url():
    '''
    If room details returned from UR Chintai API is not "null",
    that room is vacant.
    '''

    # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=000020654'

    request_sender = setup_request_sender('not null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_room_vacant(url=url)

    # Assert
    assert isVacant == True

@pytest.mark.asyncio
async def test_should_return_true_if_room_vacant_using_code():
    '''
    If room details returned from UR Chintai API is not "null",
    that room is vacant.
    '''

    # Arrange
    room_code = {
        'store_code': '40',
        'house_code': '246',
        'type': '0',
        'room_id': '000020654',
    }

    request_sender = setup_request_sender('not null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_room_vacant(room_code=room_code)

    # Assert
    assert isVacant == True

@pytest.mark.asyncio
async def test_should_return_false_if_room_full_using_url():
    '''
    If room details returned from UR Chintai API is "null",
    that room is full.
    '''

    # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=000020654'

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_room_vacant(url=url)

    # Assert
    assert isVacant == False

@pytest.mark.asyncio
async def test_should_return_false_if_room_full_using_code():
    '''
    If room details returned from UR Chintai API is "null",
    that room is full.
    '''

    # Arrange
    room_code = {
        'store_code': '40',
        'house_code': '246',
        'type': '0',
        'room_id': '000020654',
    }

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    isVacant = await client.is_room_vacant(room_code=room_code)

    # Assert
    assert isVacant == False

@pytest.mark.asyncio
async def test_should_prioritize_room_code_over_url(mocker):
    '''
    If both room code and URL are provided, use room code.
    '''

     # Arrange
    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=000020654'
    room_code = {
        'store_code': '40',
        'house_code': '246',
        'type': '0',
        'room_id': '000020654',
    }

    mock_parser = mocker.patch('urchintai_client.ur_parser.get_room_code_from_url', \
        return_value=room_code)

    request_sender = setup_request_sender('null')
    client = UrClient(request_sender)

    # Act
    await client.is_room_vacant(url=url, room_code=room_code)

    # Assert
    mock_parser.assert_not_called()

@pytest.mark.asyncio
async def test_get_property_name_should_throw_error_if_no_argument():
    '''
    Either url or room_code is required
    '''

    # Arrange
    client = UrClient(ignored_request_sender)
    urls = [None, '']

    # Act
    for url in urls:
        with pytest.raises(ValueError) as e:
            await client.get_property_name(url)

        # Assert
        assert str(e.value) == 'Room\'s URL cannot be empty'

@pytest.mark.asyncio
async def test_should_get_property_name_from_page(mocker):
    '''
    If page response contains property name, parse that value and return.
    '''

    # Arrange
    expected_property_name = 'Khu Tap The Bo Cong An'

    url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html'

    request_sender = setup_request_sender('not null', method='GET')
    mocker.patch('urchintai_client.ur_parser.get_property_name_from_content',\
        return_value=expected_property_name)

    client = UrClient(request_sender)

    # Act
    property_name = await client.get_property_name(url)

    # Assert
    assert property_name == expected_property_name

def setup_request_sender(text, method='POST'):
    resp = asyncio.Future()
    resp.set_result(text)
    request_sender = Mock()

    if method == 'POST':
        request_sender.post.return_value = resp
    else:
        request_sender.get.return_value = resp
    
    return request_sender