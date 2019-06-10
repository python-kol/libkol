from typing import Any, Coroutine, Dict, Generic, Optional, TypeVar
from yarl import URL

from aiohttp import ClientResponse

import libkol

ParserReturn = TypeVar("ParserReturn")


class Request(Generic[ParserReturn]):
    session: "libkol.Session"
    request: Coroutine[Any, Any, ClientResponse]
    response: Optional[ClientResponse] = None
    returns_json: bool = False

    def __init__(self, session: "libkol.Session"):
        self.session = session

    async def run(self) -> ClientResponse:
        self.response = await self.request
        return self.response

    async def text(self, encoding: Optional[str] = None) -> str:
        response = self.response or await self.run()

        if encoding is None:
            encoding = response.get_encoding()

        return await response.text(encoding)

    async def json(self) -> Dict[str, Any]:
        response = self.response or await self.run()

        return await response.json(content_type="text/html")

    @staticmethod
    async def parser(content, **kwargs) -> ParserReturn:
        return content

    async def parse(self, **kwargs) -> ParserReturn:
        content = await self.json() if self.returns_json else await self.text()

        assert self.response is not None

        url = self.response.url  # type: URL

        return await self.parser(content, url=url, session=self.session, **kwargs)
