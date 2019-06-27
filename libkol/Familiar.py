import asyncio
from tortoise.fields import IntField, CharField, BooleanField, ForeignKeyField
from tortoise.models import ModelMeta
from typing import Optional, Union
from dataclasses import dataclass

from .Model import Model


class FamiliarMeta(ModelMeta):
    def __getitem__(self, key: Union[int, str]):
        """
        Syntactic sugar for synchronously grabbing a Familiar by id or name.

        :param key: id or name of skill you want to grab
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def getitem():
            if isinstance(key, int):
                result = await self.get(id=key)
            else:
                result = await self.get(name=key)

            future.set_result(result)

        asyncio.ensure_future(getitem())
        return future


class Familiar(Model, metaclass=FamiliarMeta):
    id = IntField()
    name = CharField(max_length=255)
    image = CharField(max_length=255)

    # Behaviour
    stat_volley = BooleanField(default=False)
    stat_sombrero = BooleanField(default=False)
    item_drop = BooleanField(default=False)
    meat_drop = BooleanField(default=False)
    physical_attack = BooleanField(default=False)
    elemental_attack = BooleanField(default=False)
    drop = BooleanField(default=False)
    block = BooleanField(default=False)
    delevel = BooleanField(default=False)
    combat_hp = BooleanField(default=False)
    combat_mp = BooleanField(default=False)
    combat_meat = BooleanField(default=False)
    combat_stat = BooleanField(default=False)
    combat_other = BooleanField(default=False)
    post_hp = BooleanField(default=False)
    post_mp = BooleanField(default=False)
    post_meat = BooleanField(default=False)
    post_stat = BooleanField(default=False)
    post_other = BooleanField(default=False)
    passive = BooleanField(default=False)
    underwater = BooleanField(default=False)
    variable = BooleanField(default=False)

    # Related items
    hatchling = ForeignKeyField("models.Item", related_name="grows_into", null=True)
    hatchling_id: Optional[int]

    equipment = ForeignKeyField("models.Item", related_name="equipment_for", null=True)
    equipment_id: Optional[int]

    # Arena skills
    cave_match_skill = IntField(default=0)
    scavenger_hunt_skill = IntField(default=0)
    obstacle_course_skill = IntField(default=0)
    hide_and_seek_skill = IntField(default=0)

    # Pokefam
    pokefam = BooleanField(default=False)

    # Attributes
    bites = BooleanField(default=False)
    has_eyes = BooleanField(default=False)
    has_hands = BooleanField(default=False)
    has_wings = BooleanField(default=False)
    is_animal = BooleanField(default=False)
    is_bug = BooleanField(default=False)
    is_flying = BooleanField(default=False)
    is_hot = BooleanField(default=False)
    is_mechanical = BooleanField(default=False)
    is_quick = BooleanField(default=False)
    is_slayer = BooleanField(default=False)
    is_sleazy = BooleanField(default=False)
    is_undead = BooleanField(default=False)
    wears_clothes = BooleanField(default=False)

    def __ge__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, int):
            return self.id == other
        else:
            return self == other

    @property
    def have(self) -> bool:
        return self in self.kol.familiars

    @property
    def weight(self) -> Optional[int]:
        if self.have is False:
            return None

        return self.kol.familiars[self].weight
