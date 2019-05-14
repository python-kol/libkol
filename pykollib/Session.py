from .request import (
    homepageRequest,
    userProfileRequest,
    loginRequest,
    logoutRequest,
    mainRequest,
    statusRequest,
    charpaneRequest,
)
from .util.Preferences import Preferences
from . import Kmail
from . import Clan
from .Location import Location

from functools import partial
from typing import Callable, Dict, Any, Union, Optional
from urllib.parse import urlparse
from aiohttp import ClientSession, ClientResponse
import asyncio


async def parse_method(
    self: ClientResponse, encoding: Optional[str] = None, **kwargs
) -> Any:
    """This method is patched into ClientResponses"""
    if "_body" not in self or self._body is None:
        await self.read()

    if encoding is None:
        encoding = self.get_encoding()

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        partial(
            self._kol_parse,
            html=self._body.decode(encoding),
            url=self.url,
            session=self._kol_session,
            **kwargs
        ),
    )  # type: ignore


class Session:
    "This class represents a user's session with The Kingdom of Loathing."

    def __init__(self):
        super().__init__()
        self.client = ClientSession()
        self.opener = self.client
        self.is_connected = False
        self.state = {}
        self.server_url = None
        self.pwd = None
        self.clan = None
        self.kmail = Kmail.Kmail(self)

    async def __aenter__(self) -> "Session":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.is_connected:
            await self.logout()
        await self.client.close()

    async def request(
        self,
        url: str,
        method: str = "POST",
        parse: Callable[..., Dict[str, Any]] = lambda html, **kwargs: html,
        pwd: bool = False,
        **kwargs
    ):
        if urlparse(url).netloc == "":
            url = "{}/{}".format(self.server_url, url)

        if pwd:
            if "params" not in kwargs:
                kwargs["params"] = {}
            kwargs["params"]["pwd"] = self.pwd

        request = self.client.request(method, url, **kwargs)

        response = await request
        response._kol_parse = parse
        response._kol_session = self
        response.parse = parse_method.__get__(response, response.__class__)

        return response

    async def login(
        self, username: str, password: str, server_number: int = 0, stealth: bool = True
    ) -> bool:
        """
        Perform a KoL login given a username and password. A server number may also be specified
        to ensure that the user logs in using that particular server. This can be helpful
        if the user continues to be redirected to a server that is down.
        """

        # Grab the KoL homepage.
        r = await homepageRequest(self, server_number=server_number)
        self.server_url = (await r.parse())["server_url"]

        # Perform the login.
        r = await loginRequest(self, username, password, stealth=stealth)
        await r.parse()
        self.state["username"] = username

        # Loading these both makes various things work
        await mainRequest(self)
        await charpaneRequest(self)

        await self.get_status()
        await self.get_profile()

        return True

    async def join_clan(self, id: int = None, name: str = None):
        return await Clan(self, id=id, name=name).join()

    def get_username(self):
        return self.state.get("username", None)

    def get_user_id(self):
        return self.state.get("user_id", None)

    async def get_status(self):
        data = await (await statusRequest(self)).json(content_type=None)
        self.pwd = data["pwd"]
        self.state["username"] = data["name"]
        self.state["user_id"] = int(data["playerid"])
        self.state["rollover"] = int(data["rollover"])

    async def get_profile(self):
        return await (await userProfileRequest(self, self.get_user_id())).parse()

    async def adventure(
        self,
        location_id: int,
        choices: Union[Dict[str, int], Callable[[str], int]] = {},
        combat: Callable = None,
    ):
        location = Location(self, id=location_id)
        return await (await location.visit()).text()

    async def logout(self):
        "Performs a logut request, closing the session."
        await logoutRequest(self)
