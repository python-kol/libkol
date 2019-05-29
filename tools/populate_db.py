from html import unescape
from urllib import request
import re

from pykollib import db, ZapGroup, Item, FoldGroup

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


@db.connection_context()
def load_mafia_zapgroups():
    items = []

    for line in request.urlopen(ZAP_GROUPS_FILE):
        line = unescape(line.decode("utf-8"))
        if len(line) < 2 or line[0] == "#":
            continue

        group = ZapGroup().save()

        for item in Item.select().where(
            Item.name.in_([i.strip() for i in line.split(",")])
        ):
            item.zap_group = group
            items += [item]

    return items


@db.connection_context()
def load_mafia_foldgroups():
    items = []

    for line in request.urlopen(FOLD_GROUPS_FILE):
        line = unescape(line.decode("utf-8"))

        if len(line) < 2 or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 2:
            continue

        group = FoldGroup(damage_percentage=int(parts[0])).save()

        for item in Item.select().where(
            Item.name.in_([i.strip() for i in parts[1].split(",")])
        ):
            item.fold_group = group
            items += [item]

    return items


def load_mafia_items():
    items = []

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

        items += [
            Item(
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
        ]

    return items


@db.connection_context()
def load_mafia_equipment():
    type = None
    items = []

    for line in request.urlopen(EQUIPMENT_FILE):
        line = unescape(line.decode("utf-8"))
        if len(line) == 0:
            continue

        if line[0] == "#":
            if line[0].startswith("# Hats"):
                type = "hat"
            elif line[0].startswith("# Pants"):
                type = "pants"
            elif line[0].startswith("# Shirts"):
                type = "shirt"
            elif line[0].startswith("# Weapons"):
                type = "weapon"
            elif line[0].startswith("# Off-hand"):
                type = "offhand"
            elif line[0].startswith("# Accessories"):
                type = "accessory"
            elif line[0].startswith("# Containers"):
                type = "container"
            continue

        parts = line.split("\t")

        if len(parts) < 3:
            continue

        if parts[0][0] == "[" and id_duplicate_pattern.match(parts[0]):
            item = Item.get_or_none(id=get_id_from_duplicate(parts[0]))
        else:
            item = Item.get_or_none(name=parts[0])

        if item is None:
            print("Unrecognized equipment name: {}".format(parts[0]))
            continue

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

        items += [item]

    fields = [
        Item.power,
        Item.hat,
        Item.pants,
        Item.shirt,
        Item.weapon,
        Item.offhand,
        Item.accessory,
        Item.container,
        Item.weapon_type,
        Item.offhand_type,
        Item.required_muscle,
        Item.required_mysticality,
        Item.required_moxie,
    ]

    return items, fields


@db.connection_context()
def load_mafia_consumables(consumable_type):
    items = []

    for line in request.urlopen("{}{}.txt".format(mafia_data, consumable_type)):
        line = unescape(line.decode("utf-8"))

        if len(line) == 0 or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 8:
            continue

        item = Item.get_or_none(name=parts[0])

        if item is None:
            print("Unrecognized {} name: {}".format(consumable_type, parts[0]))
            continue

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

        items += [item]

    fields = [
        Item.fullness,
        Item.inebriety,
        Item.spleenhit,
        Item.level_required,
        Item.quality,
        Item.gained_adventures_min,
        Item.gained_adventures_max,
        Item.gained_muscle_min,
        Item.gained_muscle_max,
        Item.gained_mysticality_min,
        Item.gained_mysticality_max,
        Item.gained_moxie_min,
        Item.gained_moxie_max,
    ]

    return items, fields


def populate():
    db.init("./pykollib/pykollib.db")
    db.create_tables([ZapGroup, FoldGroup, Item])

    items = load_mafia_items()

    with db.atomic():
        Item.bulk_create(items, batch_size=100)

    equipment, fields = load_mafia_equipment()

    with db.atomic():
        Item.bulk_update(equipment, fields, batch_size=100)

    for c in ["fullness", "inebriety", "spleenhit"]:
        consumables, fields = load_mafia_consumables(c)

        with db.atomic():
            Item.bulk_update(consumables, fields, batch_size=100)

    zapgroups = load_mafia_zapgroups()

    with db.atomic():
        Item.bulk_update(zapgroups, [Item.zap_group], batch_size=100)

    foldgroups = load_mafia_foldgroups()

    with db.atomic():
        Item.bulk_update(foldgroups, [Item.fold_group], batch_size=100)


if __name__ == "__main__":
    populate()
