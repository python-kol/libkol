import asyncio
from tortoise import Tortoise
from tortoise.transactions import atomic
from tortoise.exceptions import DoesNotExist
from html import unescape
from urllib import request
import re

from pykollib import ZapGroup, Item, FoldGroup

mafia_data = "https://svn.code.sf.net/p/kolmafia/code/src/data/"
EQUIPMENT_FILE = "https://svn.code.sf.net/p/kolmafia/code/src/data/equipment.txt"
FOLD_GROUPS_FILE = "https://svn.code.sf.net/p/kolmafia/code/src/data/foldgroups.txt"
ITEMS_FILE = "https://svn.code.sf.net/p/kolmafia/code/src/data/items.txt"
ZAP_GROUPS_FILE = "https://svn.code.sf.net/p/kolmafia/code/src/data/zapgroups.txt"

ENCHANTMENT_MAPPINGS = {
    "Adventures": "adventuresAtRollover",
    "Cold Damage": "coldDamage",
    "Cold Resistance": "coldResistance",
    "Cold Spell Damage": "coldSpellDamage",
    "Critical": "critical",
    "Damage Absorption": "damageAbsorption",
    "Fumble": "fumble",
    "Hobo Power": "hoboPower",
    "Hot Damage": "hotDamage",
    "Hot Resistance": "hotResistance",
    "Hot Spell Damage": "hotSpellDamage",
    "Initiative": "initiative",
    "Item Drop": "itemDrop",
    "Maximum HP": "maximumHP",
    "Maximum MP": "maximumMP",
    "Meat Drop": "meatDrop",
    "Melee Damage": "weaponDamage",
    "Moxie Percent": "moxiePercent",
    "Muscle Percent": "musclePercent",
    "Mysticality Percent": "mysticalityPercent",
    "Moxie": "moxie",
    "Muscle": "muscle",
    "Mysticality": "mysticality",
    "Ranged Damage": "rangedDamage",
    "Sleaze Damage": "sleazeDamage",
    "Sleaze Resistance": "sleazeResistance",
    "Sleaze Spell Damage": "sleazeSpellDamage",
    "Spell Damage": "spellDamage",
    "Spell Damage Percent": "spellDamagePercent",
    "Spooky Damage": "spookyDamage",
    "Spooky Resistance": "spookyResistance",
    "Spooky Spell Damage": "spookySpellDamage",
    "Stench Damage": "stenchDamage",
    "Stench Resistance": "stenchResistance",
    "Stench Spell Damage": "stenchSpellDamage",
    "Weapon Damage": "weaponDamage",
}

GIFT_PACKAGES = [
    "raffle prize box",
    "Warehouse 23 crate",
    "anniversary gift box",
    "bindle of joy",
    "moist sack",
    "foreign box",
    "Uncle Crimbo's Sack",
]

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
async def load_mafia_zapgroups():
    tasks = []

    for i, line in enumerate(request.urlopen(ZAP_GROUPS_FILE)):
        line = unescape(line.decode("utf-8"))
        if len(line) < 2 or line[0] == "#":
            continue

        group = ZapGroup(index=i)

        await group.save()

        items = await Item.filter(name__in=[i.strip() for i in line.split(",")])

        for item in items:
            item.zapgroup_id = group.id
            tasks += [item.save()]

    return await asyncio.gather(*tasks)

@atomic()
async def load_mafia_foldgroups():
    tasks = []

    for line in request.urlopen(FOLD_GROUPS_FILE):
        line = unescape(line.decode("utf-8"))

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
async def load_mafia_items():
    tasks = []

    for line in request.urlopen(ITEMS_FILE):
        line = unescape(line.decode("utf-8"))

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
async def load_mafia_equipment():
    type = None
    tasks = []

    for line in request.urlopen(EQUIPMENT_FILE):
        line = unescape(line.decode("utf-8"))
        if len(line) == 0:
            continue

        if line[0] == "#":
            if line.startswith("# Hats"):
                type = "hat"
            elif line.startswith("# Pants"):
                type = "pants"
            elif line.startswith("# Shirts"):
                type = "shirt"
            elif line.startswith("# Weapons"):
                type = "weapon"
            elif line.startswith("# Off-hand"):
                type = "offhand"
            elif line.startswith("# Accessories"):
                type = "accessory"
            elif line.startswith("# Containers"):
                type = "container"
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
async def load_mafia_consumables(consumable_type):
    tasks = []

    for line in request.urlopen("{}{}.txt".format(mafia_data, consumable_type)):
        line = unescape(line.decode("utf-8"))

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


async def populate():
    await Tortoise.init(
        db_url="sqlite://pykollib/pykollib.db",
        modules={'models': ['pykollib.ZapGroup', "pykollib.FoldGroup", "pykollib.Item"]}
    )

    await Tortoise.generate_schemas(safe=True)

    print("Inserting items")
    await load_mafia_items()
    print("Updating equipable items")
    await load_mafia_equipment()

    print("Updating consumable items")
    for c in ["fullness", "inebriety", "spleenhit"]:
        await load_mafia_consumables(c)

    print("Updating zappable items")
    await load_mafia_zapgroups()
    print("Updating foldable items")
    await load_mafia_foldgroups()

    await Tortoise.close_connections()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(populate())
    loop.close()
