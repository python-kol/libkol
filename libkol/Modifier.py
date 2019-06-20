from .Model import Model
from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional


class Modifier(Model):
    item = ForeignKeyField("models.Item", related_name="modifiers", null=True)
    item_id: Optional[int]

    effect = ForeignKeyField("models.Effect", related_name="modifiers", null=True)
    effect_id: Optional[int]

    key = CharField(max_length=255)
    numeric_value = IntField(null=True)
    string_value = CharField(max_length=255, null=True)
    expression_value = CharField(max_length=255, null=True)
    percentage = BooleanField(default=False)
