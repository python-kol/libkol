import asyncio
from typing import Any, Coroutine, Dict, Optional, Tuple, Union

from aiohttp import ClientResponse
from yarl import URL

import pykollib


class Request:
    session: "pykollib.Session"
    request: Coroutine[Any, Any, ClientResponse]
    returns_json: bool = False

    def __init__(self, session: "pykollib.Session"):
        self.session = session

    async def text(self, encoding: Optional[str] = None) -> Tuple[str, URL]:
        response = await self.request

        if response.content is None:
            await response.read()

        if encoding is None:
            encoding = response.get_encoding()

        content = await response.text(encoding)

        return content, response.url

    async def json(self) -> Tuple[Dict[str, Any], URL]:
        response = await self.request

        if response.content is None:
            await response.read()

        content = await response.json()

        return content, response.url

    async def parse(self, **kwargs):
        if self.returns_json:
            content = await self.json()
        else:
            content = await self.text()

        if callable(self.parser) is False:
            return content

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.parser(content, request.url, self.session, **kwargs)
        )
