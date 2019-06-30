from tortoise.fields import IntField, CharField, BooleanField

from .Model import Model


class Trophy(Model):
    id = IntField(pk=True, generated=False)
    name = CharField(max_length=255)
    image = CharField(max_length=255)
    before_ascending = BooleanField(default=False)
    stateful = BooleanField(default=False)
