import asyncio
import pickle
from tortoise.transactions import atomic
from html import unescape
from functools import partial
from aiohttp import ClientSession
import re
from sympy import functions, Symbol
from sympy.parsing.sympy_parser import parse_expr, _token_splittable, standard_transformations, implicit_multiplication, split_symbols_custom

from typing import Any, Coroutine, List
from libkol import Modifier, Effect, Item, Skill

from util import load_mafia_data, mafia_dedupe

async def cross_referencer(name: str, value: str, modifier_base):
    name = name.lower()

    if name == "item":
        Entity = Item
    elif name == "effect":
        Entity = Effect
    elif name == "skill":
        Entity = Skill
    else:
        return False, None

    try:
        entity = await Entity.get(**mafia_dedupe(value))
    except:
        print("Couldn't find {} `{}` for modifier".format(name, value))
        return False, None

    modifier_base["{}_id".format(name)] = entity.id

    return True, entity

def can_split(symbol):
    if symbol not in Modifier.custom_functions:
        return _token_splittable(symbol)
    return False


def caret_to_pow(tokens, local_dict, global_dict):
    for i, token in enumerate(tokens):
        if token == (53, "^"):
            tokens[i] = (53, "**")

    return tokens

@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Modifier]]

    async for bytes in (await load_mafia_data(session, "modifiers")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if "\t" not in line or line[0] == "#":
            continue

        parts = line.split("\t")

        modifier_base = {}

        referencable, entity = await cross_referencer(parts[0], parts[1], modifier_base)

        if referencable is False:
           continue

        modifiers_pattern = re.compile(
            '([A-Za-z][A-Z\'a-z ]+?)( Percent)?(?:: (".*?"|\[.*?\]|[+-]?[0-9\.]+))?(?:, |$)'
        )

        for m in modifiers_pattern.finditer(parts[2]):
            modifier = Modifier(
                **modifier_base, key=m.group(1), percentage=(m.group(2) is not None)
            )

            if modifier.key == "Single Equip" and isinstance(entity, Item):
                entity.single_equip = True
                tasks += [entity.save()]
                continue

            value = m.group(3)

            if value is None:
                pass
            elif value[0] == "[":
                expr = value[1:-1]

                for f in Modifier.custom_functions.keys():
                    original = "class" if f == "charclass" else f
                    if original in expr:
                        expr = re.sub(r"{}\(([^\)]+)\)".format(original), "{}(\"\\1\")".format(f), expr)

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
                    **{f: partial(register_custom_func, f) for f in Modifier.custom_functions.keys()}
                }

                transformations = standard_transformations + (split_symbols_custom(can_split), caret_to_pow, implicit_multiplication)

                try:
                    expr = parse_expr(expr, local_dict=funcs, transformations=transformations, evaluate=True)
                except:
                    print("Failed to parse {}".format(expr))
                    continue

                modifier.pickled_expression = pickle.dumps((expr, custom_funcs))
            elif value[0] == '"':
                modifier.string_value = value[1:-1]
            else:
                modifier.numeric_value = float(value)

            tasks += [modifier.save()]

    return await asyncio.gather(*tasks)
