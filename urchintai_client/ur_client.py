# -*- coding: utf-8 -*-

from urchintai_client import ur_parser
from urchintai_client.constants import (UR_API_PROPERTY_ROOMS,
                                        UR_API_ROOM_DETAILS)


class UrClient:
    '''
    This class use UR Chintai URL to check if a property is vacant or not.
    '''

    def __init__(self, request_sender):
        self._request_sender = request_sender

    async def is_property_vacant(self, url=None, property_code=None):
        '''
        Query UR Chintai API to get the list of empty room in a property.
        If the list is empty then that property is full and vice versa.

        At least url or property_code must be provided.
        If both are provided, property_code is prioritized.
        '''

        if not url and not property_code:
            raise ValueError('Please provide either property\'s URL or property code')

        if property_code is None:
            property_code = ur_parser.get_property_code_from_url(url)

        property_data = self._build_data_from_property_code(property_code)

        resp = await self._request_sender.post(UR_API_PROPERTY_ROOMS, property_data)
        return resp != 'null'

    async def get_property_name(self, url):
        '''
        Load property page and parse html doc to retrieve property name.
        '''

        if not url:
            raise ValueError('Room\'s URL cannot be empty')

        resp = await self._request_sender.get(url)
        property_name = ur_parser.get_property_name_from_content(resp)

        return property_name

    async def is_room_vacant(self, url=None, room_code=None):
        '''
        Query UR Chintai API to check if a given room is vacant.

        At least url or room_code must be provided.
        If both are provided, room_code is prioritized.
        '''

        if not url and not room_code:
            raise ValueError('Please provide either room\'s URL or room code')

        if room_code is None:
            room_code = ur_parser.get_room_code_from_url(url)
        room_data = self._build_data_from_room_code(room_code)

        resp = await self._request_sender.post(UR_API_ROOM_DETAILS, room_data)
        return resp != 'null'

    def _build_data_from_property_code(self, property_code):
        return {
            'shisya': property_code['store_code'],
            'danchi': property_code['house_code'],
            'shikibetu': property_code['type'],
            'orderByField': '0',
            'orderBySort': '0',
            'pageIndex': '0',
        }

    def _build_data_from_room_code(self, room_code):
        return {
            'shisya': room_code['store_code'],
            'danchi': room_code['house_code'],
            'shikibetu': room_code['type'],
            'id': room_code['room_id'],
        }
