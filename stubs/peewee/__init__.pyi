from typing import Any, Iterable, Iterator, List, Optional, Type, TypeVar, overload

T = TypeVar("T")
K = TypeVar("K")

class SqliteDatabase():
    def __init__(self, file: Optional[str]) -> None: ...

    def init(self, file: str) -> None: ...

class ModelBase(type):
    def __repr__(self) -> str: ...

    def __iter__(self) -> Any: ... # ModelSelect

    @overload
    def __getitem__(self: T, key: int) -> T: ...

    @overload
    def __getitem__(self: T, key: slice) -> List[T]: ...

    def __setitem__(self: T, key: int, value: T) -> T: ...

    def __delitem__(self, key: int) -> Any: ...

    def __contains__(self: T, key: int) -> bool: ...

    def __len__(self: T) -> int: ...

    def __bool__(self: T) -> bool: ...

class Model(ModelBase):
    def __init__(self) -> None: ...

    @classmethod
    def get_or_none(cls: Type[T], **kwargs: Any) -> Optional[T]: ...


class IntegerField():
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        default: Optional[int] = None,
        **kwargs,
    ) -> None: ...

    def __get__(self, instance: Any, owner: Any) -> int: ...

class CharField():
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        default: Optional[str] = None,
    ) -> None: ...

    def __get__(self, instance: Any, owner: Any) -> str: ...

class BooleanField():
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        default: Optional[bool] = None,
    ) -> None: ...

    def __get__(self, instance: Any, owner: Any) -> bool: ...

class ForeignKeyField():
    def __init__(
        self,
        join: Type["Model"],
        null: bool = False,
        primary_key: bool = False,
        backref: Optional[str] = None,
    ) -> None: ...

    def __get__(self, instance: Any, owner: Any) -> Type["Model"]: ...
