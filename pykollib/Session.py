from .request import (
    homepageRequest,
    userProfileRequest,
    loginRequest,
    logoutRequest,
    statusRequest,
    charpaneRequest,
)
from .util.Preferences import Preferences
from . import Kmail

from typing import Callable, Dict, Any,Optional
from urllib.parse import urlparse
from aiohttp import ClientSession


async def parse_method(self, encoding: Optional[str] = None, **kwargs) -> Any:
    """This method is patched into ClientResponses"""
    if self._body is None:
        await self.read()

    if encoding is None:
        encoding = self.get_encoding()

    return await self._kol_parse(html=self._body.decode(encoding), url=self.url, session=self._kol_session, **kwargs) # type: ignore


class Session:
    "This class represents a user's session with The Kingdom of Loathing."

    def __init__(self):
        super().__init__()
        self.client = ClientSession()
        self.opener = self.client
        self.preferences = Preferences("anonymous_prefs.db", False, True)
        self.is_connected = False
        self.userId = None
        self.username = None
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

    async def post(
        self, url: str, parse: Callable[..., Dict[str, Any]] = lambda: {}, **kwargs
    ):
        if urlparse(url).netloc == "":
            url = "{}/{}".format(self.server_url, url)

        response = await self.client.post(url, **kwargs)
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

        # Load preferences for user
        self.preferences.load("{}_prefs.db".format(username), True)

        # Grab the KoL homepage.
        r = await homepageRequest(self, server_number=server_number)
        self.server_url = (await r.parse())["server_url"]

        # Perform the login.
        r = await loginRequest(self, username, password, stealth=stealth)
        login = await r.parse()
        self.username = username

        # Load the charpane once to make StatusRequest report the rollover time
        await charpaneRequest(self)

        await self.get_status()
        await self.get_profile()

        return True

    def get_username(self):
        return self.username

    async def get_status(self):
        data = await (await statusRequest(self)).json(content_type=None)
        self.pwd = data["pwd"]
        self.username = data["name"]
        self.user_id = int(data["playerid"])
        self.rollover = int(data["rollover"])

    async def get_profile(self):
        return await (await userProfileRequest(self, self.user_id)).parse()

    async def logout(self):
        "Performs a logut request, closing the session."
        await logoutRequest(self)
