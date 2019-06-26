import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "items")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) == 0 or line[0] == "#":
            continue

        parts = line.split("\t")
        if len(parts) < 3:
            continue

        use = [t.strip() for t in parts[4].split(",")]
        access = parts[5].split(",")

        plural = (
            None
            if len(parts) < 8
            else ""
            if parts[7] == "{}s".format(parts[1])
            else parts[7]
        )

        item = Item(
            id=int(parts[0]),
            name=parts[1],
            desc_id=int(parts[2]),
            image=parts[3],
            usable=any(u in use for u in ["usable", "multiple", "reusable", "message"]),
            multiusable="multiple" in use,
            reusable="reusable" in use,
            combat_usable=any(u in use for u in ["combat", "combat reusable"]),
            combat_reusable="combat reusable" in use,
            curse="curse" in use,
            bounty="bounty" in use,
            candy=2 if "candy2" in use else 1 if "candy1" in use else 0,
            hatchling="grow" in use,
            pokepill="pokepill" in use,
            food="food" in use,
            booze="drink" in use,
            spleen="spleen" in use,
            hat="hat" in use,
            weapon="weapon" in use,
            sixgun="sixgun" in use,
            offhand="offhand" in use,
            container="container" in use,
            shirt="shirt" in use,
            pants="pants" in use,
            accessory="accessory" in use,
            familiar_equipment="familiar" in use,
            sphere="sphere" in use,
            sticker="sticker" in use,
            card="card" in use,
            folder="folder" in use,
            bootspur="bootspur" in use,
            bootskin="bootskin" in use,
            food_helper="food helper" in use,
            booze_helper="drink helper" in use,
            guardian="guardian" in use,
            single_equip=False if "accessory" in use else True,
            quest="q" in access,
            gift="g" in access,
            tradeable="t" in access,
            discardable="d" in access,
            autosell=int(parts[6]),
            plural=plural,
        )

        tasks += [item._insert_instance()]

    return await asyncio.gather(*tasks)
