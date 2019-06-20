import asyncio
from tortoise.transactions import atomic
from tortoise.exceptions import DoesNotExist
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item

from util import load_mafia_data, split_range

async def load(session: ClientSession):
    for c in ["fullness", "inebriety", "spleenhit"]:
        await load_consumables(session, c)

@atomic()
async def load_consumables(session: ClientSession, consumable_type):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, consumable_type)).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) == 0 or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 8:
            continue

        try:
            item = await Item.get(name=parts[0])
        except DoesNotExist:
            print("No matching item for consumable {}".format(parts[0]))

        space = int(parts[1])
        if consumable_type == "fullness":
            item.fullness = space
        elif consumable_type == "inebriety":
            item.inebriety = space
        elif consumable_type == "spleenhit":
            item.spleenhit = space
        else:
            print("Unrecognized consumable type {}".format(consumable_type))
            return []

        item.level_required = int(parts[2])
        item.quality = parts[3]

        if parts[4] not in ["", "0"]:
            min, max = split_range(parts[4])
            item.gained_adventures_min = min
            item.gained_adventures_max = max

        if parts[5] not in ["", "0"]:
            min, max = split_range(parts[5])
            item.gained_muscle_min = min
            item.gained_muscle_max = max

        if parts[6] not in ["", "0"]:
            min, max = split_range(parts[6])
            item.gained_mysticality_min = min
            item.gained_mysticality_max = max

        if parts[7] not in ["", "0"]:
            min, max = split_range(parts[7])
            item.gained_moxie_min = min
            item.gained_moxie_max = max

        tasks += [item.save()]

    return await asyncio.gather(*tasks)
