import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, Store

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    store = None

    async for bytes in (await load_mafia_data(session, "npcstores")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2 or line[0] == "#":
            continue

        parts = line.split("\t")

        if store is None or store.slug != parts[1]:
            store = Store(name=parts[0], slug=parts[1])
            await store.save()

        item = await Item.get(name=parts[2])

        item.store_id = store.id
        item.store_price = int(parts[3])
        item.store_row = int(parts[4][3:]) if len(parts) > 4 else None

        tasks += [item.save()]

    return await asyncio.gather(*tasks)
