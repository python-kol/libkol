from .Model import Model
from tortoise.fields import CharField, IntField


class Outfit(Model):
    id = IntField(pk=True)
    name = CharField(max_length=255)
    image = CharField(max_length=255)
