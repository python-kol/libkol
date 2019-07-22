from typing import List
from tortoise.fields import BooleanField, IntField, ForeignKeyField

from .Model import Model


class MonsterDrop(Model):
    item = ForeignKeyField("models.Item", related_name="drops")
    monster = ForeignKeyField("models.Monster", related_name="drops")

    rate = IntField()
    pickpocket_only = BooleanField(default=False)
    no_pickpocket = BooleanField(default=False)
    conditional = BooleanField(default=False)
    fixed = BooleanField(default=False)
    stealable_accordion = BooleanField(default=False)
