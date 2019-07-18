from aiohttp import ClientResponse, ClientSession
from collections import defaultdict
from dataclasses import dataclass, field
from os import path
from time import time
from tortoise import Tortoise
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

import libkol
from libkol import Clan, Kmail, request, Item, Bonus, Familiar, Trophy

from .types import FamiliarState
from .Skill import Skill
from .Slot import Slot
from .Trophy import Trophy
from .Model import Model
from .Element import Element
from .Stat import Stat
from .CharacterClass import CharacterClass
from .Location import Location
from .util.decorators import logged_in

models = [
    "libkol.Bonus",
    "libkol.Effect",
    "libkol.Familiar",
    "libkol.FoldGroup",
    "libkol.Item",
    "libkol.Monster",
    "libkol.MonsterDrop",
    "libkol.MonsterImage",
    "libkol.Outfit",
    "libkol.OutfitVariant",
    "libkol.Skill",
    "libkol.Store",
    "libkol.Trophy",
    "libkol.ZapGroup",
]


@dataclass
class Stats:
    base: int = 0
    buffed: int = 0

    def from_tuple(self, tuple):
        buffed, base = tuple
        self.buffed = buffed
        self.base = base


@dataclass
class State:
    adventures: int = 0
    character_class: Optional[CharacterClass] = None
    clan: Optional[Clan] = None
    current_hp: int = 0
    current_mp: int = 0
    custom_title: Optional[str] = None
    effects: Dict[str, int] = field(default_factory=dict)
    equipment: Dict[Slot, Optional[Item]] = field(default_factory=dict)
    familiar: Optional[Familiar] = None
    familiars: Dict[Familiar, FamiliarState] = field(default_factory=defaultdict)
    fullness: int = 0
    gender: str = "n"
    inebriety: int = 0
    inventory: DefaultDict[Item, int] = field(default_factory=lambda: defaultdict(int))
    level: int = 0
    max_hp: int = 0
    max_mp: int = 0
    meat: int = 0
    ascensions: int = 0
    tattoos: int = 0
    trophies: List[Trophy] = field(default_factory=list)
    pwd: str = ""
    rollover: int = 0
    skills: List[Skill] = field(default_factory=list)
    spleenhit: int = 0
    stats: Dict[Stat, Stats] = field(
        default_factory=lambda: {
            Stat.Moxie: Stats(),
            Stat.Muscle: Stats(),
            Stat.Mysticality: Stats(),
        }
    )
    title: Optional[str] = None
    user_id: int = 0
    username: str = ""


class Session:
    "This class represents a user's session with The Kingdom of Loathing."

    user_agent = "libkol"

    def __init__(self, db_file=None):
        super().__init__()
        self.client = ClientSession()
        self.opener = self.client
        self.is_connected = False
        self.state = State()
        self.server_url = None
        self.kmail = Kmail(self)
        self.db_file = db_file or path.join(path.dirname(__file__), "libkol.db")

    async def __aenter__(self) -> "Session":
        db_url = "sqlite://{}".format(self.db_file)
        await Tortoise.init(db_url=db_url, modules={"models": models})
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
        self.state.username = username

        # Loading these both makes various things work
        await request.main(self).parse()
        await request.charpane(self).parse()

        await self.get_status()
        await self.refresh_profile()
        await self.refresh_inventory()
        await self.refresh_equipment()
        await self.refresh_familiars()
        await self.refresh_gender()
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

    @property
    def username(self) -> Optional[str]:
        """
        Returns the current player's username
        """
        return self.state.username

    @property
    def user_id(self) -> Optional[int]:
        """
        Returns the current player's user id
        """
        return self.state.user_id

    @property
    def clan(self) -> Optional[Clan]:
        """
        Returns the current player's clan
        """
        return self.state.clan

    async def get_elemental_resistance(
        self, element: Element, percentage: bool = False
    ) -> Union[float, int]:
        query = Bonus.filter(
            item_id__in=[
                item.id for item in self.equipment.values() if item is not None
            ],
            modifier=element.resistance,
        )
        flat = sum([await b.get_value() async for b in query])

        if percentage is False:
            return flat

        extra = 0.05 if self.get_character_class().stat is Stat.Mysticality else 0
        return (
            (flat * 0.1) if flat < 4 else (0.9 - (0.5 * (5 / 6) ** (flat - 4)))
        ) + extra

    @property
    def adventures(self):
        return self.state.adventures

    @property
    def hp(self):
        return self.state.current_hp

    @property
    def max_hp(self):
        return self.state.max_hp

    @property
    def mp(self):
        return self.state.current_mp

    @property
    def skills(self):
        return self.state.skills

    @property
    def pwd(self):
        return self.state.pwd

    @logged_in
    async def get_status(self) -> bool:
        """
        Load the current username, user_id, pwd and rollover time into the state
        """
        return await request.status(self).parse()

    @logged_in
    async def refresh_profile(self) -> bool:
        """
        Return information from the player's profile
        """
        user_id = self.user_id

        if user_id is None:
            return False

        profile = await request.player_profile(self, user_id).parse()

        self.state.username = profile.username
        self.state.clan = profile.clan
        self.state.ascensions = profile.ascensions
        self.state.tattoos = profile.tattoos
        self.state.trophies = profile.trophies

        return True

    @logged_in
    async def get_skills(self) -> List["libkol.Skill"]:
        """
        Return list of player's known skills
        """
        return await request.skills(self).parse()

    @logged_in
    def get_stat(self, stat: Stat, buffed: bool = False) -> int:
        stats = self.state.stats[stat]
        return stats.buffed if buffed else stats.base

    @logged_in
    def get_character_class(self) -> CharacterClass:
        return self.state.character_class

    @property
    def inebriety(self) -> int:
        return self.state.inebriety

    @property
    def fullness(self) -> int:
        return self.state.fullness

    @property
    def spleenhit(self) -> int:
        return self.state.spleenhit

    @property
    def level(self) -> int:
        return self.state.level

    @property
    def effects(self) -> Dict[str, int]:
        return self.state.effects

    @property
    def ascensions(self) -> int:
        return self.state.ascensions

    @logged_in
    async def refresh_gender(self) -> bool:
        if self.get_character_class() == CharacterClass.AstralSpirit:
            self.state.gender = "n"
        else:
            d = await (await Item["vinyl boots"]).get_description()
            self.state.gender = "f" if "+15% Moxie" in d["enchantments"] else "m"

        return True

    @property
    def gender(self) -> str:
        return self.state.gender

    @property
    def familiar(self) -> Optional[Familiar]:
        return self.state.familiar

    @property
    def familiar_weight(self) -> int:
        return self.state.familiars[self.familiar].weight

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
        return self.state.equipment

    @logged_in
    async def refresh_familiars(self) -> bool:
        await request.familiar(self).parse()
        return True

    @property
    def familiars(self) -> Dict["libkol.Familiar", "libkol.types.FamiliarState"]:
        return self.state.familiars

    @logged_in
    async def unequip(self, slot: Optional["libkol.Slot"] = None):
        return await request.unequip(self, slot).parse()

    @logged_in
    async def refresh_inventory(self) -> bool:
        await request.inventory(self).parse()
        return True

    @property
    def inventory(self) -> DefaultDict[Item, int]:
        return defaultdict(int, self.state.inventory)

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
        combat_function: Callable = None,
    ):
        """
        Run adventure in a location

        .. warning:: This method is experimental

        :param location_id: The id of the location to visit
        :param choices: Either a dictionary of choices to make, or a callable that can make that
                        decision
        :param combat_function: A function that carries out combat
        """
        location = Location(self, id=location_id)
        return await location.visit(choices, combat_function)

    @logged_in
    async def logout(self):
        """"
        Performs a logut request, closing the session.
        """
        await request.logout(self).parse()
