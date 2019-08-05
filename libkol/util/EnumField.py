from enum import Enum
from typing import Optional, Type

from tortoise.exceptions import ConfigurationError
from tortoise.fields import CharField


class EnumField(CharField):
    """
    An extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(128, **kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Optional[Enum], instance) -> Optional[str]:
        return value.value if value else None

    def to_python_value(self, value: Optional[str]) -> Optional[Enum]:
        try:
            return self._enum_type(value) if value is not None else None
        except Exception:
            raise ValueError(
                "Database value {} does not exist on Enum {}.".format(
                    value, self._enum_type
                )
            )
