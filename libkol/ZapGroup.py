from .Model import Model
from tortoise.fields import IntField


class ZapGroup(Model):
    index = IntField()
