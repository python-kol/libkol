from aiohttp import ClientSession, ClientResponse
from functools import partial
from os import path
from time import time
from typing import Callable, Coroutine, Dict, Any, Union, Optional
from urllib.parse import urlparse
import asyncio

from .request import homepage, player_profile, login, logout, main, status, charpane
from . import Kmail, Clan
from .database import db, db_kol
from .Location import Location
from .util.decorators import logged_in


async def parse_method(
    self: ClientResponse, encoding: Optional[str] = None, **kwargs
) -> Any:
    """This method is patched into ClientResponses"""
    if self.content is None:
        await self.read()

    if encoding is None:
        encoding = self.get_encoding()

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        partial(
            self._kol_parse,
            html=(await self.text(encoding)) if self._kol_json is False else None,
            json=(await self.json()) if self._kol_json is True else None,
            url=self.url,
            session=self._kol_session,
            **kwargs
        ),
    )


class Session:
    "This class represents a user's session with The Kingdom of Loathing."

    def __init__(self, db_file=None):
        super().__init__()
        self.client = ClientSession()
        self.opener = self.client
        self.is_connected = False
        self.state = {}
        self.server_url = None
        self.pwd = None
        self.clan = None
        self.kmail = Kmail.Kmail(self)
        self._db_init(db_file)

    async def __aenter__(self) -> "Session":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.is_connected:
            await self.logout()
        await self.client.close()

    def _db_init(self, db_file=None):
        if db_file is None:
            db_file = path.join(path.dirname(__file__), "pykollib.db")

        db.init(db_file)
        db_kol.init(self)

    async def request(
        self,
        url: str,
        method: str = "POST",
        parse: Callable[..., Any] = lambda html, **kwargs: html,
        pwd: bool = False,
        ajax: bool = False,
        json: bool = False,
        **kwargs
    ) -> ClientResponse:
        """
        Make an HTTP request. This is mostly proxied through to ClientRequest

        :param url: URL to request. If no host is specified, the current KoL server URL is used.
        :param method: HTTP method to use
        :param parse: Parse function to attach to the ClientResponse
        :param pwd: Whether to inject the pwd into the request
        :param ajax: Whether to inject the necessary ajax params into the request
        :param json: Whether to parse the response as JSON instead of HTML
        """
        if urlparse(url).netloc == "":
            url = "{}/{}".format(self.server_url, url)

        if "params" not in kwargs:
            kwargs["params"] = {}

        if pwd:
            kwargs["params"]["pwd"] = self.pwd

        if ajax:
            kwargs["params"]["_"] = int(time() * 1000)
            kwargs["params"]["ajax"] = 1

        request = self.client.request(method, url, **kwargs)

        response = await request
        response._kol_parse = parse
        response._kol_json = json
        response._kol_session = self
        response.parse = parse_method.__get__(response, response.__class__)

        return response

    async def parse(self, request: Callable, *args, parse_args={}, **kwargs):
        response = await request(self, *args, **kwargs)
        try:
            return await response.parse(**parse_args)
        except Exception as e:
            print(request.__name__)
            raise e

    async def login(
        self, username: str, password: str, server_number: int = 0, stealth: bool = True
    ) -> bool:
        """
        Perform a KoL login given a username and password. A server number may also be specified
        to ensure that the user logs in using that particular server. This can be helpful
        if the user continues to be redirected to a server that is down.

        :param username: Your username
        :param password: Your password
        :param server_number: Which server number to use
        :param stealth: Whether to announce your login
        """

        # Grab the KoL homepage.
        self.server_url = (
            await self.parse(homepage, server_number=server_number)
        ).server_url

        # Perform the login.
        logged_in = await self.parse(login, username, password, stealth=stealth)
        self.is_connected = logged_in
        self.state["username"] = username

        # Loading these both makes various things work
        await self.parse(main)
        await self.parse(charpane)

        await self.get_status()
        await self.get_profile()

        return True

    @logged_in
    async def join_clan(self, id: int = None, name: str = None) -> bool:
        """
        Join a clan. Either id or name must be specified.

        :param id: id of the clan to join
        :param name: Name of the clan to join
        """
        return await Clan(self, id=id, name=name).join()

    def get_username(self) -> Optional[str]:
        """
        Returns the current player's username
        """
        return self.state.get("username", None)

    def get_user_id(self) -> Optional[int]:
        """
        Returns the current player's user id
        """
        return self.state.get("user_id", None)

    @logged_in
    async def get_status(self):
        """
        Load the current username, user_id, pwd and rollover time into the state
        """
        data = await (await status(self)).json(content_type=None)
        self.pwd = data["pwd"]
        self.state["username"] = data["name"]
        self.state["user_id"] = int(data["playerid"])
        self.state["rollover"] = int(data["rollover"])

    async def get_profile(self) -> Dict[str, Any]:
        """
        Return information from the player's profile
        """
        return await self.parse(player_profile, self.get_user_id())

    @logged_in
    async def adventure(
        self,
        location_id: int,
        choices: Union[Dict[str, int], Callable[[str], int]] = {},
        combat: Callable = None,
    ):
        """
        Run adventure in a location

        .. warning:: This method is experimental

        :param location_id: The id of the location to visit
        :param choices: Either a dictionary of choices to make, or a callable that can make that
                        decision
        :param combat: A function that carries out combat
        """
        location = Location(self, id=location_id)
        return await (await location.visit()).text()

    @logged_in
    async def logout(self):
        """"
        Performs a logut request, closing the session.
        """
        await self.parse(logout)
