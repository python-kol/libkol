import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession
import re
from sympy import functions
from sympy.parsing.sympy_parser import (
    parse_expr,
    _token_splittable,
    standard_transformations,
    implicit_multiplication,
    split_symbols_custom,
)

from typing import Any, Coroutine, Dict, List, Union
from libkol import Item, Monster, MonsterImage, MonsterDrop, Element, Phylum

from util import load_mafia_data, split_range, mafia_dedupe

param_pattern = re.compile(r"(?:(\w+)(?:: +(\S+))?)")
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


def can_split(symbol):
    return False


def caret_to_pow(tokens, local_dict, global_dict):
    for i, token in enumerate(tokens):
        if token == (53, "^"):
            tokens[i] = (53, "**")

    return tokens


def parse_expression(value: str):
    funcs = {"min": functions.Min, "max": functions.Max}

    transformations = standard_transformations + (
        split_symbols_custom(can_split),
        caret_to_pow,
        implicit_multiplication,
    )

    try:
        expr = parse_expr(
            value, local_dict=funcs, transformations=transformations, evaluate=True
        )
    except:
        print("Failed to parse {}".format(value))
        return None

    return expr


def apply_params(monster: Monster, param_list: str):
    for m in re.finditer(param_pattern, param_list):
        if m[1] in param_map.keys():
            value = m[2]
            if value[0] == "[":
                value = value[1:-1]
            setattr(monster, "_" + param_map[m[1]], parse_expression(value))
        elif m[1] == "Meat":
            start, end = split_range(m[2])
            monster.meat = (start + end) / 2
        elif m[1] == "Phys":
            monster.physical_resistance = int(m[2])
        elif m[1] == "P":
            monster.phylum = Phylum(m[2])
        elif m[1] == "E":
            monster.attack_element = Element(m[2])
            monster.defence_element = Element(m[2])
        elif m[1] == "EA":
            monster.attack_element = Element(m[2])
        elif m[1] == "ED":
            monster.defence_element = Element(m[2])
        else:
            setattr(monster, m[1].lower(), True)


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
