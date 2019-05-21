from typing import NamedTuple
from peewee import IntegerField, CharField, BooleanField, ForeignKeyField

from .database import BaseModel
from .FoldGroup import FoldGroup
from .ZapGroup import ZapGroup


class Item(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    desc_id = IntegerField()
    plural = CharField(null=True)
    image = CharField()
    autosell = IntegerField(default=0)
    level_required = IntegerField(default=0)  # Level required

    # Consumables
    food = BooleanField(default=False)
    fullness = IntegerField(default=0)
    booze = BooleanField(default=False)
    inebriety = IntegerField(default=0)
    spleen = BooleanField(default=False)
    spleenhit = IntegerField(default=0)
    quality = CharField(null=True)
    gained_adventures_min = IntegerField(default=0)
    gained_adventures_max = IntegerField(default=0)
    gained_muscle_min = IntegerField(default=0)
    gained_muscle_max = IntegerField(default=0)
    gained_mysticality_min = IntegerField(default=0)
    gained_mysticality_max = IntegerField(default=0)
    gained_moxie_min = IntegerField(default=0)
    gained_moxie_max = IntegerField(default=0)

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
    weapon_hands = IntegerField(null=True)
    weapon_type = CharField(null=True)
    offhand = BooleanField(default=False)
    offhand_type = CharField(null=True)
    accessory = BooleanField(default=False)
    container = BooleanField(default=False)
    sixgun = BooleanField(default=False)
    familiar_equipment = BooleanField(default=False)
    power = IntegerField(null=True)
    required_muscle = IntegerField(default=0)
    required_mysticality = IntegerField(default=0)
    required_moxie = IntegerField(default=0)

    # Collections
    fold_group = ForeignKeyField(FoldGroup, backref="items", null=True)
    zap_group = ForeignKeyField(ZapGroup, backref="items", null=True)

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
    candy = IntegerField()  # 0: n/a, 1: simple, 2: complex
    sphere = BooleanField(default=False)  # What is this for?
    quest = BooleanField(default=False)  # is a quest item
    gift = BooleanField(default=False)  # is a gift item
    tradeable = BooleanField(default=False)  # is tradeable
    discardable = BooleanField(default=False)  # is discardable

    def pluralize(self):
        return "{}s".format(self.name) if self.plural is None else self.plural


class ItemQuantity(NamedTuple):
    item: Item
    quantity: int
