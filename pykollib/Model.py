from tortoise.models import Model as TortoiseModel
import pykollib

class Model(TortoiseModel):
    kol: "pykollib.Session"
