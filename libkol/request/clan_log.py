from enum import Enum, auto
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re

import libkol
from libkol.util import parsing

from ..Error import UnknownError
from .request import Request


class Action(Enum):
    Unknown = auto()
    Fax = auto()
    Attack = auto()
    Whitelisted = auto()
    JoinedAnother = auto()
    Joined = auto()
    Left = auto()
    Applied = auto()
    Accepted = auto()
    StashAdded = auto()
    StashTook = auto()
    StashMeat = auto()
    ChangedRank = auto()
    ChangedTitle = auto()
    DungeonOpened = auto()
    DungeonClosed = auto()
    DungeonMeat = auto()
    FloundryFabricated = auto()
    HotDogSupplied = auto()
    HotDogAte = auto()
    SpeakeasyBadPassword = auto()


@dataclass
class ClanLog:
    date: datetime
    action: Action
    user_id: Optional[int]
    username: str
    data: Dict[str, str]


user_p = r"(?P<username>.*?)(?: \(#(?P<user_id>[0-9]+)\))?"
other_user_p = r"(?P<other_username>.*?) \(#(?P<other_user_id>[0-9]+)\)"


class clan_log(Request[List[ClanLog]]):
    """
    Retrieves the clan activity log.
    """

    def __init__(self, session: "libkol.Session"):
        self.request = session.request("clan_log.php")

    log_patterns = {
        re.compile(r"^{} faxed in a (?P<monster>.*)$".format(user_p)): Action.Fax,
        re.compile(
            r"^{} added {} to the clan's whitelist\.$".format(user_p, other_user_p)
        ): Action.Whitelisted,
        re.compile(r"^{} joined another clan\.$".format(user_p)): Action.JoinedAnother,
        re.compile(r"^{} left the clan\.$".format(user_p)): Action.Left,
        re.compile(
            r"^{} was accepted into the clan \(whitelist\)$".format(user_p)
        ): Action.Joined,
        re.compile(r"^{} applied to the clan\.$".format(user_p)): Action.Applied,
        re.compile(
            r"^{} accepted {} into the clan\.$".format(user_p, other_user_p)
        ): Action.Accepted,
        re.compile(
            r"^{} added (?P<quantity>[0-9]+) (?P<item>.*?)\.$".format(user_p)
        ): Action.StashAdded,
        re.compile(
            r"^{} took (?P<quantity>[0-9]+) (?P<item>.*?)\.$".format(user_p)
        ): Action.StashTook,
        re.compile(
            r"^{} contributed (?P<amount>[0-9,]+) Meat\.$".format(user_p)
        ): Action.StashMeat,
        re.compile(
            r"^{} changed Rank for {}\.$".format(user_p, other_user_p)
        ): Action.ChangedRank,
        re.compile(
            r"^{} changed title for {}\. \((?P<title>.*?)\)$".format(
                user_p, other_user_p
            )
        ): Action.ChangedTitle,
        re.compile(
            r"^{} opened up (?P<dungeon>.*?)$".format(user_p)
        ): Action.DungeonOpened,
        re.compile(
            r"^{} (sealed|shut down) (?P<dungeon>.*?)$".format(user_p)
        ): Action.DungeonClosed,
        re.compile(
            r"^{} recovered (?P<amount>[0-9,]+) Meat from Hobopolis$".format(user_p)
        ): Action.DungeonMeat,
        re.compile(
            r"^{} fabricated a (?P<item>.*?) at the Floundry\.$".format(user_p)
        ): Action.FloundryFabricated,
        re.compile(
            r"^{} added to the hot dog cart supply \((?P<item>.*?)x(?P<quantity>[0-9]+)\)\.$".format(
                user_p
            )
        ): Action.HotDogSupplied,
        re.compile(r"^{} ate an? (?P<item>.*?)\.$".format(user_p)): Action.HotDogAte,
        re.compile(
            r"^{} gave the speakeasy bartender a bad password\.$".format(user_p)
        ): Action.SpeakeasyBadPassword,
    }

    @classmethod
    def parse_clan_log(cls, raw_log: str) -> ClanLog:
        date = datetime.strptime(raw_log[:17], "%m/%d/%y, %I:%M%p")
        log_info = raw_log[19:]
        for pattern, action in cls.log_patterns.items():
            m = pattern.match(log_info)

            if m is None:
                continue

            data = m.groupdict()

            username = data.pop("username")
            raw_user_id = data.pop("user_id", None)
            user_id = int(raw_user_id) if raw_user_id is not None else None

            return ClanLog(
                action=action, date=date, username=username, user_id=user_id, data=data
            )

        raise UnknownError("Unrecognised clan log {}".format(raw_log))

    @classmethod
    async def parser(cls, content: str, **kwargs) -> List[ClanLog]:
        soup = BeautifulSoup(content, "html.parser")

        raw_logs = [
            log.get_text()
            for section in soup.find_all("font", size=2)
            for log in parsing.split_by_br(section, soup.new_tag("div"))
        ]

        return [cls.parse_clan_log(raw_log) for raw_log in raw_logs]
