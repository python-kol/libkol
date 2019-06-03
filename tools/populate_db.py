import asyncio
from tortoise import Tortoise
from tortoise.transactions import atomic
from tortoise.exceptions import DoesNotExist
from html import unescape
from aiohttp import ClientSession, ClientResponse
import re
from typing import Any, Coroutine, List

from pykollib import ZapGroup, Item, FoldGroup, Store

async def load_mafia_data(session: ClientSession, key: str) -> ClientResponse:
    response = await session.get("https://svn.code.sf.net/p/kolmafia/code/src/data/{}.txt".format(key))
    return response

range_pattern = re.compile(r"(-?[0-9]+)(?:-(-?[0-9]+))?")


def split_range(range: str):
    m = range_pattern.match(range)

    if m is None:
        raise ValueError("Cannot split range: {}".format(range))

    start = int(m.group(1))
    return start, int(m.group(2)) if m.group(2) else start


id_duplicate_pattern = re.compile(r"\[([0-9]+)\].+")


def get_id_from_duplicate(name: str):
    m = id_duplicate_pattern.match(name)

    if m is None:
        raise ValueError("Cannot extract id from duplicate item name: {}".format(name))

    return int(m.group(1))

@atomic()
async def load_zapgroups(session: ClientSession):
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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

@atomic()
async def load_foldgroups(session: ClientSession):
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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

@atomic()
async def load_items(session: ClientSession):
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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
            usable=any(
                u in use for u in ["usable", "multiple", "reusable", "message"]
            ),
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
            drink="drink" in use,
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
            drink_helper="drink helper" in use,
            guardian="guardian" in use,
            quest="q" in access,
            gift="g" in access,
            tradeable="t" in access,
            discardable="d" in access,
            autosell=int(parts[6]),
            plural=plural,
        )

        tasks += [item._insert_instance()]

    return await asyncio.gather(*tasks)

@atomic()
async def load_equipment(session: ClientSession):
    type = None
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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

        if parts[0][0] == "[" and id_duplicate_pattern.match(parts[0]):
            items = [await Item.get(id=get_id_from_duplicate(parts[0]))]
        else:
            items = await Item.filter(name=parts[0])

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
                        'Unrecognized requirement "{}" for {}'.format(parts[2], item.name)
                    )

            tasks += [item.save()]

    return await asyncio.gather(*tasks)

@atomic()
async def load_consumables(session: ClientSession, consumable_type):
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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

@atomic()
async def load_npcstores(session: ClientSession):
    tasks = [] # type: List[Coroutine[Any, Any, Item]]

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


async def populate():
    await Tortoise.init(
        db_url="sqlite://pykollib/pykollib.db",
        modules={'models': ['pykollib.ZapGroup', "pykollib.FoldGroup", "pykollib.Item", "pykollib.Store"]}
    )

    await Tortoise.generate_schemas(safe=True)

    async with ClientSession() as session:
        print("Inserting items")
        await load_items(session)
        print("Discovering equipable items")
        await load_equipment(session)

        print("Discovering consumable items")
        for c in ["fullness", "inebriety", "spleenhit"]:
            await load_consumables(session, c)

        print("Discovering zappable items")
        await load_zapgroups(session)
        print("Discovering foldable items")
        await load_foldgroups(session)

        print("Discovering store items")
        await load_npcstores(session)

    await Tortoise.close_connections()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(populate())
    loop.close()
