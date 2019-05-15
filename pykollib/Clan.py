from math import ceil
import asyncio
from typing import List, Dict, Any

from .util.decorators import logged_in
from .request import (
    applyToClanRequest,
    clanRaidLogRequest,
    searchClansRequest,
    clanShowRequest,
    clanRaidsRequest,
    clanRanksListRequest,
    clanWhitelistRequest,
    clanRaidsPreviousRequest,
    clanStashRequest,
    clanWhitelistAddPlayerRequest,
    clanWhitelistRemovePlayerRequest,
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
        r = await searchClansRequest(self.session, self.name, exact=True)
        results = await r.parse()
        if len(results) == 0:
            raise ValueError("Cannot find clan")
        id = results[0]["id"]
        return Clan(session, id, name)

    @logged_in
    async def load(self, session):
        info = await (await clanShowRequest(self.session, self.id)).parse()
        self.leader = info["leader"]
        self.name = info["name"]
        self.website = info["website"]
        self.credo = info["credo"]

    @logged_in
    async def get_raids(self):
        r = await clanRaidsRequest(self.session)
        return await r.parse()

    @logged_in
    async def get_raid_log(self, raid_id: int):
        r = await clanRaidLogRequest(self.session, raid_id)
        return await r.parse()

    @logged_in
    async def get_stash(self):
        r = await clanStashRequest(self.session)
        return await r.parse()

    @logged_in
    async def add_user_to_whitelist(self, user, rank: int = 0, title: str = "") -> bool:
        r = await clanWhitelistAddPlayerRequest(self.session, user, rank, title)
        return (await r.parse())["success"]

    @logged_in
    async def remove_user_from_whitelist(self, user) -> bool:
        r = await clanWhitelistRemovePlayerRequest(self.session, user)
        return await r.parse()

    @logged_in
    async def get_whitelist(self, include_rank: bool = False) -> List[Dict[str, Any]]:
        r = await clanWhitelistRequest(self.session)
        return await r.parse(include_rank=include_rank)

    @logged_in
    async def get_rank_permissions(self) -> List[Dict[str, Any]]:
        r = await clanRanksListRequest(self.session)
        return await r.parse()

    @logged_in
    async def get_ranks(self) -> List[Dict[str, Any]]:
        r = await clanWhitelistRequest(self.session)
        return await r.parse(only_rank=True)

    @logged_in
    async def get_previous_raids(self, limit: int = None) -> List[Dict[str, Any]]:
        s = self.session

        raids = []

        if limit is None:
            first_page = await (await clanRaidsPreviousRequest(s, page=0)).parse()
            raids += first_page["raids"]
            limit = first_page["total"]

        tasks = []
        for page in range(ceil(limit / 10)):
            if page == 0 and len(raids) > 0:
                continue
            task = asyncio.ensure_future(clanRaidsPreviousRequest(s, page=page))
            tasks.append(task)

        r = await asyncio.gather(*tasks)
        for page in r:
            data = await page.parse()
            raids += data["raids"]

        return raids

    @logged_in
    async def join(self) -> bool:
        s = self.session

        data = await (await applyToClanRequest(s, self.id)).parse()
        return data["success"]
