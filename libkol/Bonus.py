from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional

import libkol
from .util import EnumField, PickleField, expression
from .Modifier import Modifier
from .Model import Model


class Bonus(Model):
    item: Optional["libkol.Item"] = ForeignKeyField("models.Item", related_name="bonuses", null=True)  # type: ignore
    item_id: Optional[int]

    effect: Optional["libkol.Effect"] = ForeignKeyField("models.Effect", related_name="bonuses", null=True)  # type: ignore
    effect_id: Optional[int]

    outfit: Optional["libkol.Outfit"] = ForeignKeyField("models.Outfit", related_name="bonuses", null=True)  # type: ignore
    outfit_id: Optional[int]

    familiar: Optional["libkol.Familiar"] = ForeignKeyField("models.Familiar", related_name="passive_bonuses", null=True)  # type: ignore
    familiar_id: Optional[int]

    throne_familiar: Optional["libkol.Familiar"] = ForeignKeyField("models.Familiar", related_name="throne_bonus", null=True)  # type: ignore
    throne_familiar_id: Optional[int]

    modifier: Modifier = EnumField(enum_type=Modifier)  # type: ignore
    numeric_value: Optional[int] = IntField(null=True)  # type: ignore
    string_value: str = CharField(max_length=255, null=True)  # type: ignore
    percentage: bool = BooleanField(default=False)  # type: ignore
    expression_value: Optional[str] = PickleField(null=True)  # type: ignore

    async def get_value(
        self,
        normalise: bool = False,
        smithsness: Optional[int] = None,
        familiar_weight: Optional[int] = None,
        hobo_power: Optional[int] = None,
    ):
        kol = self.kol

        if self.string_value:
            return 1

        if self.numeric_value:
            if self.percentage is False:
                return self.numeric_value

            return self.modifier.apply_percentage(kol, self.numeric_value / 100)

        if self.expression_value:
            subs = {}

            if familiar_weight is not None:
                subs["W"] = familiar_weight

            if smithsness is not None:
                subs["K"] = smithsness

            if hobo_power is not None:
                subs["H"] = hobo_power

            return await expression.evaluate(kol, self.expression_value, subs)

        return 0
