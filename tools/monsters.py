import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession
import re

from typing import Any, Coroutine, Dict, List, Union
from libkol import Item, Monster, MonsterImage, MonsterDrop, Element, Phylum
from libkol.util import expression

from util import load_mafia_data, split_range, mafia_dedupe

param_pattern = re.compile(r"(?:(?P<key>\w+)(?:: +(?P<value>\[[^\]]+\]|\S+))?)")
drop_pattern = re.compile(
    r"^(?P<item>.*?)(?: \((?P<modifier>[a-zA-Z]?)(?P<rate>\d+)\))?$"
)

param_map = {
    "Atk": "attack",
    "Cap": "cap",
    "Def": "defence",
    "Exp": "experience",
    "Floor": "floor",
    "HP": "hp",
    "Init": "initiative",
    "MLMult": "ml_factor",
    "Scale": "scale",
    "SprinkleMin": "sprinkle_min",
    "SprinkleMax": "sprinkle_max",
}


def apply_params(monster: Monster, param_list: str):
    for m in re.finditer(param_pattern, param_list):
        key, value = m.groups()
        if key in param_map.keys():
            if value[0] == "[":
                value = value[1:-1]
            setattr(monster, "_" + param_map[key], expression.parse(value))
        elif key == "Meat":
            start, end = split_range(value)
            monster.meat = (start + end) / 2
        elif key == "Phys":
            monster.physical_resistance = int(value)
        elif key == "P":
            monster.phylum = Phylum(value)
        elif key == "E":
            monster.attack_element = Element(value)
            monster.defence_element = Element(value)
        elif key == "EA":
            monster.attack_element = Element(value)
        elif key == "ED":
            monster.defence_element = Element(value)
        else:
            setattr(monster, key.lower(), True)


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Union[MonsterImage, MonsterDrop]]]

    async for bytes in (await load_mafia_data(session, "monsters")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2 or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 4:
            continue

        id = int(parts[1])

        if id == 0:
            continue

        monster = Monster(name=parts[0], id=id)
        apply_params(monster, parts[3])

        if monster.name == "Remarkable Elba Kramer":
            monster.phylum = Phylum.Dude

        await monster.save()

        for image in parts[2].split(","):
            tasks += [MonsterImage(image=image, monster=monster).save()]

        for drop in parts[4:]:
            m = re.match(drop_pattern, drop)

            if m is None:
                print(f"Couldn't parse MonsterDrop `{drop}`")
                continue

            d = m.groupdict()

            item_name = d["item"]
            rate = int(d["rate"]) if d["rate"] else 0
            mod = d["modifier"]

            if item_name == "dense Meat stack":
                item_name = item_name.lower()
            elif item_name == "boss Bat bling":
                item_name = "Boss Bat bling"
            elif item_name == "Greek Fire":
                item_name = "Greek fire"
            elif item_name in ["giant X (100n)", "giant O (100n)"]:
                item_name = item_name[0:7]
                rate = 100
                mod = "n"
            elif item_name == "negative lump (0))":
                item_name = "negative lump"

            item = await Item.filter(**mafia_dedupe(item_name)).first()

            monster_drop = MonsterDrop(item=item, monster=monster, rate=rate)

            if mod == "p":
                monster_drop.pickpocket_only = True
            elif mod == "n":
                monster_drop.no_pickpocket = True
            elif mod == "c":
                monster_drop.conditional = True
            elif mod == "f":
                monster_drop.fixed = True
            elif mod == "a":
                monster_drop.stealable_accordion = True

            tasks += [monster_drop.save()]

    return await asyncio.gather(*tasks)
