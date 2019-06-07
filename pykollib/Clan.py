import asyncio
from math import ceil
from typing import Any, Dict, List

from . import request
from .request.clan_raids_previous import Raid
from .util.decorators import logged_in


class Clan(object):
    "This class represents a Clan in the Kingdom of Loathing"

    def __init__(self, session, id, name=None):
        self.session = session
        self.id = id
        self.name = name
        self.leader = None
        self.website = None
        self.credo = None

    @classmethod
    @logged_in
    async def find(self, session, name):
        results = await request.clan_search(session, self.name, exact=True).parse()
        if len(results) == 0:
            raise ValueError("Cannot find clan")
        id = results[0]["id"]
        return Clan(session, id, name)

    @logged_in
    async def load(self, session):
        info = await request.clan_show(session, self.id).parse()
        self.leader = info["leader"]
        self.name = info["name"]
        self.website = info["website"]
        self.credo = info["credo"]

    @logged_in
    async def get_raids(self):
        return await request.clan_raids(self.session).parse()

    @logged_in
    async def get_raid_log(self, raid_id: int):
        return await request.clan_raid_log(self.session, raid_id).parse()

    @logged_in
    async def get_stash(self):
        return await request.clan_stash(self.session).parse()

    @logged_in
    async def add_user_to_whitelist(self, user, rank: int = 0, title: str = "") -> bool:
        return (
            await request.clan_whitelist_add(self.session, user, rank, title).parse()
        ).success

    @logged_in
    async def remove_user_from_whitelist(self, user) -> bool:
        return await request.clan_whitelist_remove(self.session, user).parse()

    @logged_in
    async def get_whitelist(self, include_rank: bool = False) -> List[Dict[str, Any]]:
        return await request.clan_whitelist(self.session).parse()

    @logged_in
    async def get_rank_permissions(self) -> List[Dict[str, Any]]:
        return await request.clan_ranks(self.session).parse()

    @logged_in
    async def get_ranks(self) -> List[Dict[str, Any]]:
        return await request.clan_whitelist(self.session).parse(only_rank=True)

    @logged_in
    async def get_previous_raids(self, limit: int = None) -> List[Raid]:
        s = self.session

        raids = []  # type: List[Raid]

        if limit is None:
            first_page = await request.clan_raids_previous(s, page=0).parse()
            raids += first_page.raids
            limit = first_page.total

        requests = [
            request.clan_raids_previous(s, page=page)
            for page in range(ceil(limit / 10))
            if page != 0 or len(raids) == 0
        ]

        await asyncio.gather(*[r.text() for r in requests])
        for r in requests:
            raids += (await r.parse()).raids

        return raids

    @logged_in
    async def join(self) -> bool:
        return (await request.clan_apply(self.session, self.id).parse()).success
