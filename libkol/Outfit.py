import libkol
from typing import List
from tortoise.fields import CharField, IntField

from .Model import Model


class Outfit(Model):
    id = IntField(pk=True, generated=False)
    name = CharField(max_length=255)
    image = CharField(max_length=255)
    variants: List["libkol.OutfitVariant"]

    async def is_fulfilled(self, equipment: List["libkol.Item"]):
        # Doesn't cover if you need more than one of an item to fulfil an outfit
        await self.fetch_related("variants", "variants__pieces")
        return any(
            all(p in equipment for p in variant.pieces) for variant in self.variants
        )
