from tortoise.fields import IntField, CharField

from .Model import Model


class Store(Model):
    name = CharField(max_length=255)
    slug = CharField(max_length=255)
