import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, ZapGroup

from util import load_mafia_data

@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    index = 1

    async for bytes in (await load_mafia_data(session, "zapgroups")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2 or line[0] == "#":
            continue

        group = ZapGroup(index=index)
        index += 1

        await group.save()

        items = await Item.filter(name__in=[i.strip() for i in line.split(",")])

        for item in items:
            item.zapgroup_id = group.id
            tasks += [item.save()]

    return await asyncio.gather(*tasks)
