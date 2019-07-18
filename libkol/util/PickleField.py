from typing import Any
import dill
import base64

from sympy.core.function import Function, UndefinedFunction
from tortoise.fields import CharField


@dill.register(UndefinedFunction)
def save_function(pickler, obj):
    pickler.save_reduce(Function, (repr(obj),), obj=obj)


class PickleField(CharField):
    """
    An extension to CharField that pickles objects
    to and from a str representation in the DB.
    """

    def __init__(self, *args, default=None, **kwargs):
        super().__init__(*args, max_length=255, default=default, **kwargs)

    @staticmethod
    def encode(value: Any) -> str:
        if value is None:
            return ""

        p = dill.dumps(value)

        return base64.b64encode(p).decode("ascii")

    def to_db_value(self, value: Any, instance) -> str:
        return self.encode(value)

    def to_python_value(self, value: str) -> Any:
        if value == "":
            return None

        p = base64.b64decode(value.encode("ascii"))
        return dill.loads(p)
