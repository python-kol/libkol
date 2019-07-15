import libkol
from enum import Enum
from typing import List, Optional
from tortoise.fields import CharField, IntField, BooleanField

from .util import EnumField, PickleField
from .Model import Model
from .Element import Element
from .Phylum import Phylum


class Monster(Model):
    id = IntField(pk=True, generated=False)
    name = CharField(max_length=255)

    # Flags
    boss = BooleanField(default=False)
    free = BooleanField(default=False)
    nobanish = BooleanField(default=False)
    nocopy = BooleanField(default=False)
    nomanuel = BooleanField(default=False)
    semirare = BooleanField(default=False)
    superlikely = BooleanField(default=False)
    ultrarare = BooleanField(default=False)
    wanderer = BooleanField(default=False)
    nowander = BooleanField(default=False)
    dummy = BooleanField(default=False)
    ghost = BooleanField(default=False)

    # Variable Stats
    attack = PickleField()
    cap = PickleField(default=10000)
    defence = PickleField()
    experience = PickleField(default=0)
    floor = PickleField(default=10)
    hp = PickleField()
    initiative = PickleField()
    ml_factor = PickleField(default=1)
    scale = PickleField(default=0)
    sprinkle_max = PickleField(default=0)
    sprinkle_min = PickleField(default=0)

    # Static stats
    attack_element = EnumField(enum_type=Element, null=True)
    defence_element = EnumField(enum_type=Element, null=True)
    meat = IntField(default=0)
    phylum = EnumField(enum_type=Phylum, null=True)
    physical_resistance = IntField(default=0)

    @classmethod
    async def identify(cls, name: str, image: Optional[str] = None) -> "Monster":
        if image is not None:
            from .MonsterImage import MonsterImage

            monster_image = await MonsterImage.get(image=image).prefetch_related(
                "monster"
            )
            return monster_image.monster

        if name.startswith(("a ", "an")):
            name = name[name.find(" ") :]

        return cls.get(name=name)
