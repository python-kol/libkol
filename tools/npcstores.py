import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, Store

from util import load_mafia_data

coinmaster_data = {
    "Bounty Hunter Hunter": ("bounty.php", "filthy lucre"),
    "Big Brother": ("monkeycastle.php", "sand dollar"),
    "Your Campfire": ("campfire", "stick of firewood"),
}


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    store = None

    for datafile in ["npcstores", "coinmasters"]:
        async for bytes in (await load_mafia_data(session, datafile)).content:
            line = unescape(bytes.decode("utf-8")).strip()

            if len(line) < 2 or line[0] == "#":
                continue

            parts = line.split("\t")

            if store is None or store.name != parts[0]:
                if datafile == "npcstores":
                    slug = parts[1]
                    token = None
                elif parts[0] not in coinmaster_data:
                    print(f"Don't know about the coinmaster `{parts[0]}`")
                    continue
                else:
                    slug, currency = coinmaster_data[parts[0]]
                    token = await Item[currency]

                store = Store(name=parts[0], slug=slug)
                await store.save()

                if token is not None:
                    token.currency_in = store
                    await token.save()

            if datafile == "npcstores":
                item_name, price, row = (parts + [None])[2:5]
                buy = "buy"
            else:
                buy, price, item_name, row = (parts + [None])[1:5]

            item = await Item[item_name]
            item.store_id = store.id
            item.store_price = price
            item.store_row = int(row[3:]) if row else None
            item.store_buy = buy == "buy"

            tasks += [item.save()]

    return await asyncio.gather(*tasks)
