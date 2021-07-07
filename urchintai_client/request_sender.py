# -*- coding: utf-8 -*-

class RequestSender:
    '''
    This class is used to make HTTP request to remote server.
    '''

    def __init__(self, session):
        self._session = session

    async def post(self, url, data):
        async with self._session.post(url, data=data) as response:
            return await self._ensure_success(url, response)

    async def get(self, url):
        async with self._session.get(url) as response:
            return await self._ensure_success(url, response)

    async def _ensure_success(self, url, response):
        status = response.status
        response_text = await response.text()

        if status == 200:
            return response_text
        else:
            raise ConnectionError(f'An error occurred while sending request to {url}: {response_text}')
