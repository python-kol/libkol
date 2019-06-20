import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item

from util import load_mafia_data, mafia_dedupe

@atomic()
async def load(session: ClientSession):
    type = None
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "equipment")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2:
            continue

        if line[0] == "#":
            type = {
                "Hats": "hat",
                "Pants": "pants",
                "Shirts": "shirt",
                "Weapons": "weapon",
                "Off-hand": "offhand",
                "Accessories": "accessory",
                "Containers": "container",
            }.get(line[2:])

        if type is None:
            continue

        parts = line.split("\t")

        if len(parts) < 3:
            continue

        items = await Item.filter(*mafia_dedupe(parts[0]))

        if len(items) == 0 or (None in items):
            print("Unrecognized equipment name: {}".format(parts[0]))
            continue

        for item in items:
            item.power = int(parts[1])
            item.hat = type == "hat"
            item.pants = type == "pants"
            item.shirt = type == "shirt"
            item.weapon = type == "weapon"
            item.offhand = type == "offhand"
            item.accessory = type == "accessory"
            item.container = type == "container"

            if len(parts) > 3:
                if item.weapon:
                    item.weapon_type == parts[3]
                elif item.offhand:
                    item.offhand_type == parts[3]

            # Set the requirements
            reqs = parts[2].strip()
            if len(reqs) > 0 and reqs != "none":
                stat = reqs[0:3]
                required = int(reqs[5:])
                if stat == "Mus":
                    item.required_muscle = required
                elif stat == "Mys":
                    item.required_mysticality = required
                elif stat == "Mox":
                    item.required_moxie = required
                else:
                    print(
                        'Unrecognized requirement "{}" for {}'.format(
                            parts[2], item.name
                        )
                    )

            tasks += [item.save()]

    return await asyncio.gather(*tasks)
