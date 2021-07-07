# -*- coding: utf-8 -*-

import aiohttp

class SessionManager:
    _session = None

    @classmethod
    def GetSession(cls):
        if not cls._session:
            cls._session = aiohttp.ClientSession()

        return cls._session

    @classmethod
    async def CloseSession(cls):
        if cls._session:
            await cls._session.close()

        cls._session = None
