import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item

from util import load_mafia_data, mafia_dedupe


@atomic()
async def load(session: ClientSession):
    equipment_type = None
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "equipment")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2:
            continue

        if line[0] == "#":
            equipment_type = {
                "Hats": "hat",
                "Pants": "pants",
                "Shirts": "shirt",
                "Weapons": "weapon",
                "Off-hand": "offhand",
                "Accessories": "accessory",
                "Containers": "container",
            }.get(line[2 : line.find(" ", 2)], equipment_type)

            continue

        parts = line.split("\t")

        if equipment_type is None or len(parts) < 3:
            continue

        items = await Item.filter(**mafia_dedupe(parts[0]))

        if len(items) == 0 or (None in items):
            print("Unrecognized equipment name: {}".format(parts[0]))
            continue

        for item in items:
            item.power = int(parts[1])
            item.hat = equipment_type == "hat"
            item.pants = equipment_type == "pants"
            item.shirt = equipment_type == "shirt"
            item.weapon = equipment_type == "weapon"
            item.offhand = equipment_type == "offhand"
            item.accessory = equipment_type == "accessory"
            item.container = equipment_type == "container"

            if len(parts) > 3:
                if item.weapon:
                    item.weapon_hands = int(parts[3][0])
                    item.weapon_type = parts[3][8:]
                elif item.offhand:
                    item.offhand_type = parts[3]

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
