from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional

from .util import EnumField, PickleField
from .Modifier import Modifier
from .Model import Model
from .koldate import koldate

from .Error import UnknownError


class Bonus(Model):
    item = ForeignKeyField("models.Item", related_name="bonuses", null=True)
    item_id: Optional[int]

    effect = ForeignKeyField("models.Effect", related_name="bonuses", null=True)
    effect_id: Optional[int]

    outfit = ForeignKeyField("models.Outfit", related_name="bonuses", null=True)
    outfit_id: Optional[int]

    modifier = EnumField(enum_type=Modifier)
    numeric_value = IntField(null=True)
    string_value = CharField(max_length=255, null=True)
    percentage = BooleanField(default=False)
    expression_value = PickleField(null=True)

    custom_functions = {
        "charclass": (lambda c: 1 if Bonus.kol.get_character_class().value == c else 0),
        "effect": lambda effect: 0,
        "env": lambda env: 0,
        "event": lambda event: 0,
        "loc": lambda loc: 0,
        "mod": lambda mod: 0,
        "path": lambda path: 0,
        "pref": lambda pref: 0,
        "skill": lambda name: next(
            (1 for s in Bonus.kol.state["skills"] if s.name == name), 0
        ),
        "zone": lambda zone: 0,
    }

    async def get_value(self, normalise: bool = False, smithsness: int = 0):
        kol = self.kol

        if self.string_value:
            return 1

        if self.numeric_value:
            if self.percentage is False:
                return self.numeric_value

            return self.modifier.apply_percentage(kol, self.numeric_value / 100)

        if self.expression_value:
            today = koldate.today()

            expression, expression_symbols = self.expression_value

            symbols = {
                "A": kol.get_num_ascensions(),
                "D": kol.get_inebriety(),
                "G": today.grimace_darkness,
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
                    UnknownError(
                        "Unknown symbols {} in {}".format(expr.free_symbols, expression)
                    )
            except Exception:
                UnknownError("Could not parse {}".format(expression))

        return 0
