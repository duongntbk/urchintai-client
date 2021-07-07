# -*- coding: utf-8 -*-

import pytest
from urchintai_client.ur_parser import (get_property_code_from_url,
                                        get_property_name_from_content,
                                        get_room_code_from_url)


def test_should_parse_property_codes_from_url():
    '''
    Can extract store code, house code and type from an UR Chintai URL.
    '''

    # Arrange
    urls = [
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/04_4121.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_0001.html'
    ]

    property_codes = [
        CreatePropertyCode("40", "412", "0"),
        CreatePropertyCode("04", "412", "1"),
        CreatePropertyCode("40", "000", "1")
    ]

    for url, property_code in zip(urls, property_codes):
        # Act
        actual_property_code = get_property_code_from_url(url)

        # Assert
        assert actual_property_code['store_code'] == property_code['store_code']
        assert actual_property_code['house_code'] == property_code['house_code']
        assert actual_property_code['type'] == property_code['type']

def test_shoud_throw_exception_if_cannot_parse_property_url():
    '''
    UR Chintai URL must be in the correct format to be parse.
    '''

    # Arrange
    urls = [
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_412.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/044121.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/044121',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa.html'
        'abcxyz'
    ]

    for url in urls:
        # Act
        with pytest.raises(ValueError) as e:
            get_property_code_from_url(url)

        # Assert
        assert str(e.value) == f'UR Chintai URL is invalid: {url}'

def test_shoud_throw_exception_if_property_url_is_null():
    '''
    Null guard.
    '''

    # Arrange, Act
    with pytest.raises(ValueError) as e:
        get_property_code_from_url(None)

    # Assert
    assert str(e.value) == 'UR Chintai URL cannot be empty'

def test_should_parse_room_codes_from_url():
    '''
    Can extract store code, house code and type and room id from an UR Chintai URL.
    '''

    # Arrange
    urls = [
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=000020654',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/04_2460_room.html?JKSS=000010653',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_0001_room.html?JKSS=000000123'
    ]

    room_codes = [
        CreateRoomCode("40", "246", "0", "000020654"),
        CreateRoomCode("04", "246", "0", "000010653"),
        CreateRoomCode("40", "000", "1", "000000123")
    ]

    for url, room_code in zip(urls, room_codes):
        # Act
        actual_room_code = get_room_code_from_url(url)

        # Assert
        assert actual_room_code['store_code'] == room_code['store_code']
        assert actual_room_code['house_code'] == room_code['house_code']
        assert actual_room_code['type'] == room_code['type']
        assert actual_room_code['room_id'] == room_code['room_id']

def test_shoud_throw_exception_if_room_url_is_null():
    '''
    Null guard.
    '''

    # Arrange,  Act
    with pytest.raises(ValueError) as e:
        get_room_code_from_url(None)

    # Assert
    assert str(e.value) == 'UR Chintai URL cannot be empty'

def test_should_throw_exception_if_cannot_parse_room_url():
    '''
    UR Chintai URL must be in the correct format to be parse.
    '''

    # Arrange
    urls = [
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_412.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKS=000020312',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKST=000020312',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=00002031',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=0000203111',
        'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html',
        'abcxyz'
    ]

    for url in urls:
        # Act
        with pytest.raises(ValueError) as e:
            get_room_code_from_url(url)

        # Assert
        assert str(e.value) == f'UR Chintai URL is invalid: {url}'

def test_should_parse_property_name_from_html_doc():
    '''
    If property page can be loaded, property name is displayed in
    a child span of header with "article_headings" class.
    All blank characters also should be removed.
    '''

    # Arrange
    expected_property_name = 'Expected Property Name'

    names_in_html_doc = [
        'Expected Property Name',
        '   Expected Property Name   ',
        '\tExpected Property Name\t',
        '\nExpected Property Name\n',
    ]

    for name_in_html_doc in names_in_html_doc:
        resp_content = '<div class="article_contents_head">' + \
                            '<div class="item_upper">' + \
                                '<h1 class="article_headings">' + \
                                    '<span class="item_title">' + \
                                        name_in_html_doc + \
                                    '</span>' + \
                                    '<span class="item_sub">' + \
                                        '(神奈川県川崎市川崎区)' + \
                                    '</span>' + \
                                '</h1>' + \
                                '<ul class="article_buttons">' + \
                                    '<li class="item_buttons_list">' + \
                                        '<a href="#list" target="_blank" class="item_button button_check_room">' + \
                                            '空室を確認' + \
                                        '</a>' + \
                                    '</li>' + \
                                    '<li class="item_buttons_list">' + \
                                        '<button class="button_bookmark js-bookmark-item" data-bookmark-kbn="KFDC" data-bookmark-key="40_1830"></button>' + \
                                    '</li>' + \
                                '</ul>' + \
                            '</div>' + \
                        '</div>'

        # Act
        property_name = get_property_name_from_content(resp_content)

        # Assert
        assert property_name == expected_property_name

def test_should_throw_error_if_cannot_find_property_name_in_html_doc():
    '''
    If cannot parse property name from html_doc, throw error.
    '''

    # Arrange
    resp_contents = [
        '',
        '<body><h1>This is a header</h1></body>',
        '<h1 class="article_headings"><span>Dummy</span><h1>',
        '<h1 class="test"><span class="item_title">Dummy</span><h1>',
        '<h1 class="article_headings"><span class="item_sub">Dummy</span><h1>'
    ]

    for resp_content in resp_contents:
        # Act
        with pytest.raises(Exception) as e:
            get_property_name_from_content(resp_content)

        # Assert
        assert str(e.value) == 'Cannot parse property name from html doc'

def CreatePropertyCode(store_code, house_code, type):
    return {
        'store_code': store_code,
        'house_code': house_code,
        'type': type
    }

def CreateRoomCode(store_code, house_code, type, room_id):
    return {
        'store_code': store_code,
        'house_code': house_code,
        'type': type,
        'room_id': room_id
    }
