import asyncio
from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from tortoise.models import ModelMeta
from typing import List, Optional, Union

from libkol import request
from .Model import Model
from .Error import ItemNotFoundError, WrongKindOfItemError
from . import types


class ItemMeta(ModelMeta):
    def __getitem__(self, key: Union[int, str]):
        """
        Syntactic sugar for synchronously grabbing an item by id, description id or name.

        :param key: id, desc_id or name of item you want to grab
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def getitem():
            if isinstance(key, int):
                # Most desc_ids are 9 digits but there are 14 that aren't.
                # At time of writing this is good for 115,100 new items before any collisions.
                if key == 31337 or key == 46522 or key >= 125353:
                    result = await self.get_or_discover(desc_id=key)
                else:
                    result = await self.get_or_discover(id=key)
            else:
                result = await self.get(name=key)

            future.set_result(result)

        asyncio.ensure_future(getitem())
        return future


class Item(Model, metaclass=ItemMeta):
    id = IntField()
    name = CharField(max_length=255)
    desc_id = IntField()
    plural = CharField(max_length=255, null=True)
    image = CharField(max_length=255)
    autosell = IntField(default=0)
    level_required = IntField(default=0)  # Level required

    # Consumables
    food = BooleanField(default=False)
    fullness = IntField(default=0)
    booze = BooleanField(default=False)
    inebriety = IntField(default=0)
    spleen = BooleanField(default=False)
    spleenhit = IntField(default=0)
    quality = CharField(max_length=255, null=True)
    gained_adventures_min = IntField(default=0)
    gained_adventures_max = IntField(default=0)
    gained_muscle_min = IntField(default=0)
    gained_muscle_max = IntField(default=0)
    gained_mysticality_min = IntField(default=0)
    gained_mysticality_max = IntField(default=0)
    gained_moxie_min = IntField(default=0)
    gained_moxie_max = IntField(default=0)

    # Usability
    usable = BooleanField(default=False)
    multiusable = BooleanField(default=False)
    combat_usable = BooleanField(default=False)
    reusable = BooleanField(default=False)
    combat_reusable = BooleanField(default=False)
    curse = BooleanField(default=False)  # Can be used on others

    # Equipment
    hat = BooleanField(default=False)
    pants = BooleanField(default=False)
    shirt = BooleanField(default=False)
    weapon = BooleanField(default=False)
    weapon_hands = IntField(null=True)
    weapon_type = CharField(max_length=255, null=True)
    offhand = BooleanField(default=False)
    offhand_type = CharField(max_length=255, null=True)
    accessory = BooleanField(default=False)
    container = BooleanField(default=False)
    sixgun = BooleanField(default=False)
    familiar_equipment = BooleanField(default=False)
    power = IntField(null=True)
    required_muscle = IntField(default=0)
    required_mysticality = IntField(default=0)
    required_moxie = IntField(default=0)

    # Collections
    foldgroup = ForeignKeyField("models.FoldGroup", related_name="items", null=True)
    foldgroup_id: Optional[int]
    zapgroup = ForeignKeyField("models.ZapGroup", related_name="items", null=True)
    zapgroup_id: Optional[int]

    # NPC Store Info
    store_row = IntField(null=True)
    store_price = IntField(null=True)
    store = ForeignKeyField("models.Store", related_name="items", null=True)
    store_id: Optional[int]

    # Flags
    hatchling = BooleanField(default=False)
    pokepill = BooleanField(default=False)
    sticker = BooleanField(default=False)
    card = BooleanField(default=False)
    folder = BooleanField(default=False)
    bootspur = BooleanField(default=False)
    bootskin = BooleanField(default=False)
    food_helper = BooleanField(default=False)
    drink_helper = BooleanField(default=False)
    guardian = BooleanField(default=False)
    bounty = BooleanField(default=False)  # Can appear as a bounty item
    candy = IntField()  # 0: n/a, 1: simple, 2: complex
    sphere = BooleanField(default=False)  # What is this for?
    quest = BooleanField(default=False)  # is a quest item
    gift = BooleanField(default=False)  # is a gift item
    tradeable = BooleanField(default=False)  # is tradeable
    discardable = BooleanField(default=False)  # is discardable

    def pluralize(self):
        return "{}s".format(self.name) if self.plural is None else self.plural

    @classmethod
    async def get_or_discover(cls, *args, **kwargs) -> "Item":
        result = await cls.filter(*args, **kwargs).first()

        if result is None:
            id: int = kwargs.get("id", None)
            desc_id: int = kwargs.get("desc_id", None)

            return await cls.discover(id=id, desc_id=desc_id)

        return result

    @classmethod
    async def discover(cls, id: int = None, desc_id: int = None):
        """
        Discover this item using its id or description id. The description id is preferred as
        it provides more information, so if only an id is provided, libkol will first determine
        the desc_id.

        Note that this Returns an Item object but it is not automatically committed to the database.
        It is not sufficient to run `await item.save()` to do this however as tortoise-orm will attempt to
        `UPDATE` the row because it already has an `id` set. Instead you need to run
        `awaititem._insert_instance()` explicitly.


        :param id: Id of the item to discover
        :param desc_id: Description id of the item to discover
        """
        if id is not None:
            desc_id = (await request.item_information(cls.kol, id).parse()).descid

        if desc_id is None:
            raise ItemNotFoundError(
                "Cannot discover an item without either an id or a desc_id"
            )

        info = await request.item_description(cls.kol, desc_id).parse()
        return Item(**{k: v for k, v in info.items() if v is not None})

    async def get_mall_price(self, limited: bool = False) -> int:
        """
        Get the lowest price for this item in the mall

        :param limited: Include limited sales in this search
        """
        prices = await request.mall_price(self.kol, self).parse()

        if limited:
            return prices.limited[0].price

        return prices.unlimited[0].price

    async def get_mall_listings(self, **kwargs) -> List["types.Listing"]:
        return await request.mall_search(self.kol, query=self, **kwargs).parse()

    async def buy_from_mall(
        self,
        listing: "types.Listing" = None,
        store_id: int = None,
        price: int = 0,
        quantity: int = 1,
    ):
        if listing is None and store_id is None:
            listings = await self.get_mall_listings(
                num_results=quantity, max_price=price
            )
            tasks = [
                request.mall_purchase(self.kol, item=self, listing=l).parse()
                for l in listings
            ]
            return await asyncio.gather(*tasks)

        return await request.mall_purchase(
            self.kol,
            item=self,
            listing=listing,
            store_id=store_id,
            price=price,
            quantity=quantity,
        ).parse()

    def amount(self):
        return self.kol.state["inventory"][self]

    async def use(self, quantity: int = 1, multi_use: bool = True):
        if self.usable is False:
            raise WrongKindOfItemError("This item cannot be used")

        if self.multiusable and multi_use:
            await request.item_multi_use(self.kol, self, quantity).parse()
            return

        tasks = [request.item_use(self.kol, self).parse() for _ in range(quantity)]
        return await asyncio.gather(*tasks)
