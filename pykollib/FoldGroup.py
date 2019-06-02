from .Model import Model
from tortoise.fields import IntField


class FoldGroup(Model):
    damage_percentage = IntField()
