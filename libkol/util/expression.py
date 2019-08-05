from sympy import functions, Expr, Function, Symbol
from sympy.parsing.sympy_parser import parse_expr
import re
from typing import Callable, Dict
import base64

import libkol
from ..Stat import Stat
from ..koldate import koldate
from ..Error import UnknownError

state_functions = {
    "charclass": lambda kol, c: 1 if kol.get_character_class().value == c else 0,
    "effect": lambda kol, effect: 0,
    "env": lambda kol, env: 0,
    "event": lambda kol, event: 0,
    "loc": lambda kol, loc: 0,
    "mod": lambda kol, mod: 0,
    "path": lambda kol, path: 0,
    "pref": lambda kol, pref: 0,
    "skill": lambda kol, name: next((1 for s in kol.skills if s.name == name), 0),
    "zone": lambda kol, zone: 0,
    "equipped": lambda kol, item: 1 if item in kol.equipment.values() else 0,
}  # type: Dict[str, Callable[[libkol.Session, str], int]]

sympy_replacements = {
    "abs": functions.Abs,
    "min": functions.Min,
    "max": functions.Max,
    "sqrt": functions.sqrt,
    "ceil": functions.ceiling,
    "floor": functions.floor,
    "N": Symbol("N"),
    "I": Symbol("I"),
}


def arg_encode(v: str):
    encoded = base64.b32encode(v.encode())
    return encoded.decode().rstrip("=")


def arg_decode(v: str):
    repadded = v + ("=" * ((8 - (len(v) % 8)) % 8))
    return base64.b32decode(repadded.encode()).decode()


def parse(expression_string: str) -> Expr:
    if expression_string == "?":
        return None

    # This is way easier than tokenizing and transforming but will break if a function argument
    # (like a skill or path) contains ^
    expression_string = expression_string.replace("^", "**")

    for f in state_functions.keys():
        original = "class" if f == "charclass" else f
        if original in expression_string:
            expression_string = re.sub(
                rf"{original}\(([^\)]+)\)",
                lambda x: f'{f}("{arg_encode(x[1])}")',
                expression_string,
            )

    try:
        return parse_expr(expression_string, local_dict=sympy_replacements)
    except Exception as e:
        print(e)
        print(f"Failed to parse `{expression_string}`")
        return None


async def evaluate(
    kol: "libkol.Session", expression: Expr, subs: Dict[str, int] = {}
) -> int:
    today = koldate.today()

    symbols = {
        "A": kol.ascensions,
        "D": kol.inebriety,
        "G": today.grimace_darkness,
        "H": 0,  # hobopower
        "J": 1 if today.jarlsberg else 0,
        "K": 0,  # smithsness,
        "L": kol.level,
        "M": today.moonlight,
        "N": 0,  # audience
        "R": await kol.get_reagent_potion_duration(),
        "W": kol.familiar_weight,
        "X": 1 if kol.gender == "f" else 0,
        "Y": kol.fury,
        "MUS": kol.get_stat(Stat.Muscle, buffed=True),
        "MYS": kol.get_stat(Stat.Mysticality, buffed=True),
        "MOX": kol.get_stat(Stat.Moxie, buffed=True),
        "ML": 0,  # Total +ML Modifier
        "MCD": 0,  # mind-control
        "HP": kol.max_hp,
        "BL": 0,  # basement level
    }

    for token, impl in state_functions.items():
        f = Function(token)
        expression = expression.replace(f, lambda sym: impl(kol, arg_decode(str(sym))))

    try:
        result = expression.evalf(subs={**symbols, **subs})
        if isinstance(result, int) or result.is_number:
            return result
        else:
            raise UnknownError(
                "Unknown symbols {} in {}".format(result.free_symbols, expression)
            )
    except Exception:
        raise UnknownError("Could not parse {}".format(expression))
