import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, Outfit

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "outfits")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2:
            continue

        parts = line.split("\t")

        if len(parts) < 4:
            continue

        outfit = Outfit(id=int(parts[0]), name=parts[1], image=parts[2])

        await outfit._insert_instance()

        items = await Item.filter(name__in=[i.strip() for i in parts[3].split(",")])

        for item in items:
            item.outfit_id = outfit.id
            tasks += [item.save()]

    return await asyncio.gather(*tasks)
