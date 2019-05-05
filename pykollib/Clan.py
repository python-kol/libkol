from math import ceil
import asyncio

from .request import (
    applyToClanRequest,
    clanRaidLogRequest,
    searchClansRequest,
    clanRaidsRequest,
    clanRaidsPreviousRequest,
)


class Clan(object):
    "This class represents a Clan in the Kingdom of Loathing"

    def __init__(self, session, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Must specify a name or id for a clan")

        self.session = session
        self.id = id
        self.name = name

    async def get_id(self):
        if self.id is None:
            r = await searchClansRequest(self.session, self.name, exact=True)
            data = await r.parse()
            results = data["results"]
            if len(results) == 0:
                raise ValueError("Clan {} does not exist".format(self.name))
            self.id = results[0]["id"]

        return self.id

    async def get_raids(self):
        r = await clanRaidsRequest(self.session)
        return await r.parse()

    async def get_raid_log(self, raid_id):
        r = await clanRaidLogRequest(self.session, raid_id)
        return await r.parse()

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

    async def join(self):
        s = self.session
        async with applyToClanRequest(s, self.id) as r:
            data = await r.parse()
            return data["success"]
