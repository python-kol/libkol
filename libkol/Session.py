from os import path
from time import time
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse
from tortoise import Tortoise
from collections import defaultdict
from aiohttp import ClientResponse, ClientSession
import libkol
from libkol import Clan, Kmail, request, Item

from .Model import Model
from .Stat import Stat
from .CharacterClass import CharacterClass
from .Location import Location
from .util.decorators import logged_in

models = [
    "libkol.FoldGroup",
    "libkol.Item",
    "libkol.ZapGroup",
    "libkol.Store",
    "libkol.Trophy",
    "libkol.Bonus",
    "libkol.Effect",
    "libkol.Skill",
    "libkol.Outfit",
]


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
        self.kmail = Kmail(self)
        self.db_file = db_file or path.join(path.dirname(__file__), "libkol.db")

    async def __aenter__(self) -> "Session":
        await Tortoise.init(
            db_url="sqlite://{}".format(self.db_file), modules={"models": models}
        )
        Model.kol = self
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.is_connected:
            await self.logout()
        await self.client.close()
        await Tortoise.close_connections()

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

        return await self.client.request(method, url, **kwargs)

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
            await request.homepage(self, server_number=server_number).parse()
        ).server_url

        # Perform the login.
        logged_in = await request.login(
            self, username, password, stealth=stealth
        ).parse()
        self.is_connected = logged_in
        self.state["username"] = username

        # Loading these both makes various things work
        await request.main(self).parse()
        await request.charpane(self).parse()

        await self.get_status()
        await self.get_profile()
        await self.refresh_inventory()
        await self.refresh_equipment()
        await self.get_skills()

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
        data = await request.status(self).parse()
        self.pwd = data["pwd"]
        self.state["username"] = data["name"]
        self.state["user_id"] = int(data["playerid"])
        self.state["rollover"] = int(data["rollover"])

    @logged_in
    async def get_profile(self) -> Dict[str, Any]:
        """
        Return information from the player's profile
        """
        user_id = self.get_user_id()

        if user_id is None:
            return {}

        return await request.player_profile(self, user_id).parse()

    @logged_in
    async def get_skills(self) -> List["libkol.Skill"]:
        """
        Return list of player's known skills
        """
        return await request.skills(self).parse()

    @logged_in
    def get_stat(self, stat: Stat, buffed: bool = False) -> int:
        return self.state["{}_{}".format("buffed" if buffed else "base", stat.value)]

    @logged_in
    def get_character_class(self) -> CharacterClass:
        return self.state["character_class"]

    @logged_in
    def get_inebriety(self) -> int:
        return self.state["inebriety"]

    @logged_in
    def get_level(self) -> int:
        return self.state["level"]

    @logged_in
    def get_num_ascensions(self) -> int:
        return self.state["num_ascensions"]

    @logged_in
    async def get_gender(self) -> str:
        if "gender" in self.state:
            pass
        elif self.get_character_class() == CharacterClass.AstralSpirit:
            self.state["gender"] = "n"
        else:
            d = await (await Item["vinyl boots"]).get_description()
            self.state["gender"] = "f" if "+15% Moxie" in d["enchantments"] else "m"

        return self.state["gender"]

    @logged_in
    def get_familiar_weight(self) -> int:
        return self.state["familiar"]["weight"]

    @logged_in
    async def get_reagent_potion_duration(self) -> int:
        from . import Skill

        duration = 5
        duration += 5 if self.get_character_class() == CharacterClass.Sauceror else 0
        duration += 5 if (await Skill["Impetuous Sauciness"]).have() else 0
        return duration

    @logged_in
    async def refresh_equipment(self) -> bool:
        await request.equipment(self).parse()
        return True

    @property
    def equipment(self) -> Dict["libkol.Slot", Optional[Item]]:
        return self.state["equipment"]

    @logged_in
    async def unequip(self, slot: Optional["libkol.Slot"] = None):
        return await request.unequip(self, slot).parse()

    @logged_in
    async def refresh_inventory(self) -> bool:
        await request.inventory(self).parse()
        return True

    @property
    def inventory(self) -> DefaultDict[Item, int]:
        return defaultdict(int, self.state["inventory"])

    @logged_in
    async def mine(
        self,
        mine_id: int,
        reset: bool = False,
        coords: Optional[Tuple[int, int]] = None,
    ):
        return await request.mining(self, mine_id, reset=reset, coords=coords).parse()

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
        await request.logout(self).parse()
