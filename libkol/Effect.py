from .Model import Model
from tortoise.fields import IntField, CharField


class Effect(Model):
    id = IntField(pk=True, generated=False)
    name = CharField(max_length=255)
    image = CharField(max_length=255)
    desc_id = CharField(max_length=255)
