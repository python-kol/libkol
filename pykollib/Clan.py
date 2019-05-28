from math import ceil
import asyncio
from typing import List, Dict, Any

from .util.decorators import logged_in
from .request import (
    clan_apply,
    clan_raid_log,
    clan_search,
    clan_show,
    clan_raids,
    clan_ranks,
    clan_whitelist,
    clan_raids_previous,
    clan_stash,
    clan_whitelist_add,
    clan_whitelist_remove,
)


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
        results = await session.parse(clan_search, self.name, exact=True)
        if len(results) == 0:
            raise ValueError("Cannot find clan")
        id = results[0]["id"]
        return Clan(session, id, name)

    @logged_in
    async def load(self, session):
        info = await session.parse(clan_show, self.id)
        self.leader = info["leader"]
        self.name = info["name"]
        self.website = info["website"]
        self.credo = info["credo"]

    @logged_in
    async def get_raids(self):
        return await self.session.parse(clan_raids)

    @logged_in
    async def get_raid_log(self, raid_id: int):
        return await self.session.parse(clan_raid_log, raid_id)

    @logged_in
    async def get_stash(self):
        return await self.session.parse(clan_stash)

    @logged_in
    async def add_user_to_whitelist(self, user, rank: int = 0, title: str = "") -> bool:
        return await self.session.parse(clan_whitelist_add, user, rank, title)

    @logged_in
    async def remove_user_from_whitelist(self, user) -> bool:
        return await self.session.parse(clan_whitelist_remove, user)

    @logged_in
    async def get_whitelist(self, include_rank: bool = False) -> List[Dict[str, Any]]:
        return await self.session.parse(clan_whitelist)

    @logged_in
    async def get_rank_permissions(self) -> List[Dict[str, Any]]:
        return await self.session.parse(clan_ranks)

    @logged_in
    async def get_ranks(self) -> List[Dict[str, Any]]:
        return await self.session.parse(clan_whitelist, parse_args={"only_rank": True})

    @logged_in
    async def get_previous_raids(self, limit: int = None) -> List[Dict[str, Any]]:
        s = self.session

        raids = []

        if limit is None:
            first_page = await s.parse(clan_raids_previous, page=0)
            raids += first_page["raids"]
            limit = first_page["total"]

        tasks = []
        for page in range(ceil(limit / 10)):
            if page == 0 and len(raids) > 0:
                continue
            task = asyncio.ensure_future(clan_raids_previous(s, page=page))
            tasks.append(task)

        r = await asyncio.gather(*tasks)
        for page in r:
            data = await page.parse()
            raids += data["raids"]

        return raids

    @logged_in
    async def join(self) -> bool:
        return (await self.session.parse(clan_apply, self.id)).success
