from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional

from .util import EnumField, PickleField, expression
from .Modifier import Modifier
from .Model import Model

from .Error import UnknownError


class Bonus(Model):
    item = ForeignKeyField("models.Item", related_name="bonuses", null=True)
    item_id: Optional[int]

    effect = ForeignKeyField("models.Effect", related_name="bonuses", null=True)
    effect_id: Optional[int]

    outfit = ForeignKeyField("models.Outfit", related_name="bonuses", null=True)
    outfit_id: Optional[int]

    familiar = ForeignKeyField(
        "models.Familiar", related_name="passive_bonuses", null=True
    )
    familiar_id: Optional[int]

    throne_familiar = ForeignKeyField(
        "models.Familiar", related_name="throne_bonus", null=True
    )
    throne_familiar_id: Optional[int]

    modifier = EnumField(enum_type=Modifier)
    numeric_value = IntField(null=True)
    string_value = CharField(max_length=255, null=True)
    percentage = BooleanField(default=False)
    expression_value = PickleField(null=True)

    async def get_value(
        self,
        normalise: bool = False,
        smithsness: Optional[int] = None,
        familiar_weight: Optional[int] = None,
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

            return await expression.evaluate(kol, self.expression_value, subs)

        return 0
