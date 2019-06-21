import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, FoldGroup

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "foldgroups")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2 or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 2:
            continue

        group = FoldGroup(damage_percentage=int(parts[0]))

        await group.save()

        items = await Item.filter(name__in=[i.strip() for i in parts[1].split(",")])

        for item in items:
            item.foldgroup_id = group.id
            tasks += [item.save()]

    return await asyncio.gather(*tasks)
