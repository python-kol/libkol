from typing import List
from tortoise.fields import CharField, ForeignKeyField

from .Model import Model


class MonsterImage(Model):
    image = CharField(max_length=255)
    monster = ForeignKeyField("models.Monster", related_name="images")
