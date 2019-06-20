from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional
from sympy import Symbol
import pickle

from .Model import Model
from .Stat import Stat
from .koldate import koldate


class Modifier(Model):
    item = ForeignKeyField("models.Item", related_name="modifiers", null=True)
    item_id: Optional[int]

    effect = ForeignKeyField("models.Effect", related_name="modifiers", null=True)
    effect_id: Optional[int]

    outfit = ForeignKeyField("models.Outfit", related_name="modifiers", null=True)
    outfit_id: Optional[int]

    key = CharField(max_length=255)
    numeric_value = IntField(null=True)
    string_value = CharField(max_length=255, null=True)
    pickled_expression = CharField(max_length=255, null=True)
    percentage = BooleanField(default=False)

    @property
    def expression_value(self):
        if self.pickled_expression is None:
            return None
        b = eval(self.pickled_expression)
        return pickle.loads(b)

    custom_functions = {
        "charclass": lambda c: 1
        if Modifier.kol.get_character_class().value == c
        else 0,
        "effect": lambda effect: 0,
        "env": lambda env: 0,
        "event": lambda event: 0,
        "loc": lambda loc: 0,
        "mod": lambda mod: 0,
        "path": lambda path: 0,
        "pref": lambda pref: 0,
        "skill": lambda name: next(
            (1 for s in Modifier.kol.state["skills"] if s.name == name), 0
        ),
        "zone": lambda zone: 0,
    }

    async def get_value(self, smithsness: int = 0):
        kol = self.kol

        if self.id == 11045:
            print(expression)

        if self.string_value:
            return 1

        if self.numeric_value:
            if self.percentage is False:
                return self.numeric_value

            base = 1
            multiplier = self.numeric_value / 100

            if self.key == "Maximum HP":
                base = kol.get_stat(Stat.Muscle, buffed=true) + 3
                multiplier += 1.5 if kol.get_character_class() in Stat.Muscle else 1
            elif self.key == "Maximum MP":
                base = kol.get_stat(Stat.Mysticality, buffed=true) + 3
                multiplier = 1.5 if kol.get_character_class() in Stat.Mysticality else 1
            elif self.key == "Muscle":
                base = base = kol.get_stat(Stat.Muscle)
            elif self.key == "Mysticality":
                base = base = kol.get_stat(Stat.Mysticality)
            elif self.key == "Moxie":
                base = base = kol.get_stat(Stat.Moxie)

            return multiplier * base

        if self.expression_value:
            today = koldate.today()

            expression, expression_symbols = self.expression_value

            symbols = {
                "A": kol.get_num_ascensions(),
                "D": kol.get_inebriety(),
                "G": today.grimace_darkness * 10,
                "K": smithsness,
                "L": kol.get_level(),
                "M": today.moonlight,
                "R": await kol.get_reagent_potion_duration(),
                "W": kol.get_familiar_weight(),
                "X": 1 if (await kol.get_gender()) == "f" else 0,
            }

            for f, a in expression_symbols:
                symbols[f] = self.custom_functions[f](a)

            try:
                expr = expression.evalf(subs=symbols)
                if isinstance(expr, int) or expr.is_number:
                    return expr
                else:
                    print(
                        "Unknown symbols {} in {}".format(expr.free_symbols, expression)
                    )
            except Exception as e:
                print("Could not parse {}".format(expression))
                print(e)

        return 0
