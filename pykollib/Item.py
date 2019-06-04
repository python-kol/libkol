from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from typing import Optional

from .Model import Model
from .Error import ItemNotFoundError
from .request import item_information, item_description as item_description_module

item_description = item_description_module.item_description # type: ignore

class Item(Model):
    id = IntField(pk=True)
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
        if id is not None:
            desc_id = (await item_information(cls.kol, id).parse()).descid

        if desc_id is None:
            raise ItemNotFoundError("Cannot discover an item without either an id or a desc_id")

        info = await item_description(cls.kol, desc_id).parse()
        return Item(**{k: v for k, v in info.items() if v is not None})
