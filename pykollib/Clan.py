from math import ceil
import asyncio

from .util.decorators import logged_in
from .request import (
    applyToClanRequest,
    clanRaidLogRequest,
    searchClansRequest,
    clanRaidsRequest,
    clanWhitelistRequest,
    clanRaidsPreviousRequest,
    clanStashRequest,
    clanWhitelistAddPlayerRequest,
    clanWhitelistRemovePlayerRequest,
)


class Clan(object):
    "This class represents a Clan in the Kingdom of Loathing"

    def __init__(self, session, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Must specify a name or id for a clan")

        self.session = session
        self.id = id
        self.name = name

    @logged_in
    async def get_id(self):
        if self.id is None:
            r = await searchClansRequest(self.session, self.name, exact=True)
            data = await r.parse()
            results = data["results"]
            if len(results) == 0:
                raise ValueError("Clan {} does not exist".format(self.name))
            self.id = results[0]["id"]

        return self.id

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
    async def add_user_to_whitelist(self, user, rank: int = 0, title: str = ""):
        r = await clanWhitelistAddPlayerRequest(self.session, user, rank, title)
        return (await r.parse())["success"]

    @logged_in
    async def remove_user_from_whitelist(self, user):
        r = await clanWhitelistRemovePlayerRequest(self.session, user)
        return await r.parse()

    @logged_in
    async def get_whitelist(self, include_rank: bool = False):
        r = await clanWhitelistRequest(self.session, include_rank)
        return await r.parse()

    @logged_in
    async def get_previous_raids(self, limit=None):
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
    async def join(self):
        s = self.session

        data = await (await applyToClanRequest(s, self.id)).parse()
        return data["success"]
