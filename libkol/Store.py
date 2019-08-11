from typing import List, Optional
from tortoise.fields import CharField

import libkol
from libkol import request
from .Error import WrongKindOfItemError
from .Model import Model


class Store(Model):
    name: str = CharField(max_length=255) # type: ignore
    slug: str = CharField(max_length=255) # type: ignore
    currency: Optional["libkol.Item"]
    items: List["libkol.Item"]

    async def buy(self, item: "libkol.Item", quantity: int = 1):
        await self.fetch_related("items")
        if item not in self.items:
            raise WrongKindOfItemError("You cannot buy that item from this store")

        return await request.npc_buy(self.kol, self, item, quantity).parse()
