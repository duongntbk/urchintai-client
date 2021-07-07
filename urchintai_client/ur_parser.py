# -*- coding: utf-8 -*-

'''
Methods to parse URL and HTMLDOC and retrieve data.
'''

import re

from bs4 import BeautifulSoup


def get_property_code_from_url(url):
    '''
    URL of a property has the following format: https://www.ur-net.go.jp/chintai/area/prefecture/AA_BBBC.html
    Where AA, BBB and C are number:
    - AA: store code
    - BBB: house code
    - C: type
    '''

    if url is None:
        raise ValueError('UR Chintai URL cannot be empty')

    reg = r'^https:\/\/www\.ur-net\.go\.jp\/chintai\/\w+\/\w+\/(\d{2})_(\d{3})(\d{1}).html$'
    match = re.search(reg, url)

    if match is None:
        raise ValueError(f'UR Chintai URL is invalid: {url}')

    return {
        'store_code': match.group(1),
        'house_code': match.group(2),
        'type': match.group(3)
    }

def get_room_code_from_url(url):
    '''
    URL of a room has the following format: https://www.ur-net.go.jp/chintai/kanto/kanagawa/AA_BBBC_room.html?JKSS=DDDDDDDDD
    Where AA, BBB, C and DDDDDDDDD are number:
    - AA: store code
    - BBB: house code
    - C: type
    - DDDDDDDDD: room code
    '''

    if url is None:
        raise ValueError('UR Chintai URL cannot be empty')

    reg = r'^https:\/\/www\.ur-net\.go\.jp\/chintai\/\w+\/\w+\/(\d{2})_(\d{3})(\d{1})_room.html\?JKSS=(\d{9})$'
    match = re.search(reg, url)

    if match is None:
        raise ValueError(f'UR Chintai URL is invalid: {url}')

    return {
        'store_code': match.group(1),
        'house_code': match.group(2),
        'type': match.group(3),
        'room_id': match.group(4),
    }

def get_property_name_from_content(html_doc):
    '''
    Property's name is not included in API response.
    We need to load the page and parse property's name from HTML doc.
    '''

    soup = BeautifulSoup(html_doc, 'html.parser')

    article_headings = soup.find_all('h1', attrs={'class':'article_headings'})
    if not article_headings:
        raise Exception('Cannot parse property name from html doc')
    article_heading = article_headings[0]

    item_title_spans = article_heading.find_all('span', attrs={'class':'item_title'})
    if not item_title_spans:
        raise Exception('Cannot parse property name from html doc')
    item_title_span = item_title_spans[0]

    property_name_with_blank = item_title_span.string
    property_name = property_name_with_blank.strip()
    return property_name
