from typing import Any
import pickle
import base64

from tortoise.fields import CharField


class PickleField(CharField):
    """
    An extension to CharField that pickles objects
    to and from a str representation in the DB.
    """

    def __init__(self, *args, default=None, **kwargs):
        d = self.encode(default) if default is not None else None
        super().__init__(*args, max_length=255, default=d, **kwargs)

    @staticmethod
    def encode(value: Any) -> str:
        if value is None:
            return ""

        p = pickle.dumps(value)
        return base64.b64encode(p).decode("ascii")

    def to_db_value(self, value: Any, instance) -> str:
        return self.encode(value)

    def to_python_value(self, value: str) -> Any:
        if value == "":
            return None

        p = base64.b64decode(value.encode("ascii"))
        return pickle.loads(p)
