import asyncio
from tortoise.fields import IntField, CharField, BooleanField
from tortoise.models import ModelMeta
from typing import Union

from .Model import Model


class SkillMeta(ModelMeta):
    def __getitem__(self, key: Union[int, str]):
        """
        Syntactic sugar for synchronously grabbing a skill by id or name.

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


class Skill(Model, metaclass=SkillMeta):
    id = IntField(pk=True, generated=False)
    name = CharField(max_length=255)
    image = CharField(max_length=255)
    autosell = IntField(default=0)
    level_required = IntField(default=0)
    mp_cost = IntField(default=0)

    passive = BooleanField(default=False)
    noncombat = BooleanField(default=False)
    shruggable = BooleanField(default=False)
    combat = BooleanField(default=False)
    healing = BooleanField(default=False)
    summon = BooleanField(default=False)
    expression = BooleanField(default=False)
    walk = BooleanField(default=False)
    mutex_song = BooleanField(default=False)

    def have(self):
        return self in self.kol.state["skills"]
