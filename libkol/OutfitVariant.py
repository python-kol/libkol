from typing import List
from tortoise.fields import ForeignKeyField

import libkol
from .Model import Model


class OutfitVariant(Model):
    outfit = ForeignKeyField("models.Outfit", related_name="variants")
    outfit_id: int
    pieces: List["libkol.Item"]
