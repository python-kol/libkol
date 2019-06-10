from tortoise.models import Model as TortoiseModel
import libkol


class Model(TortoiseModel):
    kol: "libkol.Session"
