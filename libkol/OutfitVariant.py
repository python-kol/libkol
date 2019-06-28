from tortoise.fields import ForeignKeyField

from .Model import Model


class OutfitVariant(Model):
    outfit = ForeignKeyField("models.Outfit", related_name="variants")
    outfit_id: int
