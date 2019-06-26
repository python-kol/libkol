import asyncio
from tortoise.transactions import atomic
from html import unescape
from functools import partial
from aiohttp import ClientSession
import re
from sympy import functions, Symbol
from sympy.parsing.sympy_parser import (
    parse_expr,
    _token_splittable,
    standard_transformations,
    implicit_multiplication,
    split_symbols_custom,
)
from typing import Any, Coroutine, Dict, List

from libkol import Bonus, Effect, Item, Modifier, Skill, Outfit, Familiar

from util import load_mafia_data, mafia_dedupe


class ModifierError(Exception):
    modifier: str

    def __init__(self, message, modifier: str):
        self.modifier = modifier


async def cross_referencer(name: str, value: str, modifier_base):
    name = name.lower()
    field = name

    name_to_ent = {
        "item": Item,
        "effect": Effect,
        "skill": Skill,
        "outfit": Outfit,
        "familiar": Familiar,
        "throne": Familiar,
    }

    Entity = name_to_ent.get(name, None)

    if name == "throne":
        field = "throne_familiar"

    if Entity is None:
        return False, None

    try:
        entity = await Entity.get(**mafia_dedupe(value))
    except:
        print("Couldn't find {} `{}` for modifier".format(name, value))
        return False, None

    modifier_base["{}_id".format(field)] = entity.id

    return True, entity


def can_split(symbol):
    if symbol not in Bonus.custom_functions:
        return _token_splittable(symbol)
    return False


def caret_to_pow(tokens, local_dict, global_dict):
    for i, token in enumerate(tokens):
        if token == (53, "^"):
            tokens[i] = (53, "**")

    return tokens


def parse_expression(expr: str):
    for f in Bonus.custom_functions.keys():
        original = "class" if f == "charclass" else f
        if original in expr:
            expr = re.sub(
                r"{}\(([^\)]+)\)".format(original), '{}("\\1")'.format(f), expr
            )

    custom_funcs = []

    def register_custom_func(f_name, arg):
        custom_funcs.append((f_name, arg))
        return Symbol(f_name)

    funcs = {
        "abs": functions.Abs,
        "min": functions.Min,
        "max": functions.Max,
        "sqrt": functions.sqrt,
        "ceil": functions.ceiling,
        "floor": functions.floor,
        "A": Symbol("A"),
        "B": Symbol("B"),
        "C": Symbol("C"),
        "D": Symbol("D"),
        "E": Symbol("E"),
        "F": Symbol("F"),
        "G": Symbol("G"),
        "H": Symbol("H"),
        "I": Symbol("I"),
        "J": Symbol("J"),
        "K": Symbol("K"),
        "L": Symbol("L"),
        "M": Symbol("M"),
        "N": Symbol("N"),
        "P": Symbol("P"),
        "R": Symbol("R"),
        "S": Symbol("S"),
        "T": Symbol("T"),
        "U": Symbol("U"),
        "W": Symbol("W"),
        "X": Symbol("X"),
        "Y": Symbol("Y"),
        **{f: partial(register_custom_func, f) for f in Bonus.custom_functions.keys()},
    }

    transformations = standard_transformations + (
        split_symbols_custom(can_split),
        caret_to_pow,
        implicit_multiplication,
    )

    try:
        expr = parse_expr(
            expr, local_dict=funcs, transformations=transformations, evaluate=True
        )
    except:
        print("Failed to parse {}".format(expr))
        return None

    return expr, custom_funcs


async def load_bonus(base, info, entity):
    key = info["key"]

    if key == "none":
        return None
    elif key == "Single Equip" and isinstance(entity, Item):
        entity.single_equip = True
        return entity.save()
    elif key == "Volleyball Effectiveness":
        print(entity.id)
        bonus = await Bonus.get(familiar_id=entity.id, modifier=Modifier.Experience)
    elif key == "Fairy Effectiveness":
        bonus = await Bonus.get(familiar_id=entity.id, modifier=Modifier.ItemDrop)
    elif key == "Leprechaun Effectiveness":
        bonus = await Bonus.get(familiar_id=entity.id, modifier=Modifier.MeatDrop)
    else:
        try:
            modifier = Modifier(key)
        except ValueError:
            raise ModifierError(
                "Modifier `{}` not recognised".format(key), modifier=key
            )

        bonus = Bonus(
            **base, modifier=modifier, percentage=(info.get("percentage") is not None)
        )

    value = info.get("value")

    if value is None:
        pass
    elif value[0] == "[":
        expr = value[1:-1]
        factor = bonus.expression_value or 1
        bonus.expression_value = factor * parse_expression(expr)
    elif value[0] == '"':
        bonus.string_value = value[1:-1]
    else:
        bonus.numeric_value = float(value)

    return bonus.save()


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Bonus]]

    unknown_modifiers = set()

    async for bytes in (await load_mafia_data(session, "modifiers")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if "\t" not in line or line[0] == "#":
            continue

        parts = line.split("\t")

        if parts[1] == "(none)":
            continue

        base = {}  # type: Dict[str, Any]
        referencable, entity = await cross_referencer(parts[0], parts[1], base)

        if referencable is False:
            continue

        bonuses_pattern = re.compile(
            '(?P<key>[A-Za-z][A-Z\'a-z ]+?)(?P<percentage> Percent)?(?:: (?P<value>".*?"|\[.*?\]|[+-]?[0-9\.]+))?(?:, |$)'
        )

        for m in bonuses_pattern.finditer(parts[2]):
            try:
                task = await load_bonus(base, m.groupdict(), entity)
            except ModifierError as e:
                unknown_modifiers.add(e.modifier)
                continue

            if task is not None:
                tasks += [task]

    if len(unknown_modifiers) > 0:
        print("Unrecognised modifiers: {}".format(", ".join(unknown_modifiers)))

    return await asyncio.gather(*tasks)
