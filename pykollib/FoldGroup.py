from peewee import IntegerField

from .database import BaseModel


class FoldGroup(BaseModel):
    damage_percentage = IntegerField()
