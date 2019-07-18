import libkol
from enum import Enum
from typing import Dict, List, Optional
from tortoise.fields import CharField, IntField, BooleanField

from .util import EnumField, PickleField, expression
from .Model import Model
from .Element import Element
from .Phylum import Phylum
from .Stat import Stat


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
    _attack = PickleField()
    _cap = PickleField(default=10000)
    _defence = PickleField()
    _experience = PickleField(default=0)
    _floor = PickleField(default=10)
    _hp = PickleField()
    _initiative = PickleField()
    _ml_factor = PickleField(default=1)
    _scale = PickleField(default=0)
    _sprinkle_max = PickleField(default=0)
    _sprinkle_min = PickleField(default=0)

    # Static stats
    attack_element = EnumField(enum_type=Element, null=True)
    defence_element = EnumField(enum_type=Element, null=True)
    meat = IntField(default=0)
    phylum = EnumField(enum_type=Phylum, null=True)
    physical_resistance = IntField(default=0)

    async def get_cap(self) -> int:
        return await expression.evaluate(self.kol, self._cap)

    async def get_floor(self) -> int:
        return await expression.evaluate(self.kol, self._floor)

    async def get_scale(self) -> int:
        return await expression.evaluate(self.kol, self._scale)

    async def get_attack(self) -> int:
        return await expression.evaluate(self.kol, self._attack)

    async def get_defence(self) -> int:
        return await expression.evaluate(self.kol, self._defence)

    async def get_hp(self) -> int:
        if self._hp is not None:
            return max(await expression.evaluate(self.kol, self._hp), 1)

        if self.get_scale() is None:
            return -1

        hp = min(
            self.get_cap(),
            max(self.get_floor(), self.kol.get_stat(Stat.Muscle, buffed=True)),
        )

        return max(hp // (4 / 3), 1)

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

        return await cls.get(name=name)
