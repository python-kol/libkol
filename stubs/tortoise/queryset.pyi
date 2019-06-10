# Stubs for tortoise.queryset (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.utils import QueryAsyncIterator
from typing import Any

class AwaitableQuery:
    model: Any = ...
    query: Any = ...
    capabilities: Any = ...
    def __init__(self, model: Any) -> None: ...
    def resolve_filters(self, model: Any, q_objects: Any, annotations: Any, custom_filters: Any) -> None: ...
    def resolve_ordering(self, model: Any, orderings: Any, annotations: Any) -> None: ...
    def __await__(self): ...

class QuerySet(AwaitableQuery):
    fields: Any = ...
    def __init__(self, model: Any) -> None: ...
    def filter(self, *args: Any, **kwargs: Any) -> "QuerySet": ...
    def exclude(self, *args: Any, **kwargs: Any) -> "QuerySet": ...
    def order_by(self, *orderings: str) -> "QuerySet": ...
    def limit(self, limit: int) -> "QuerySet": ...
    def offset(self, offset: int) -> "QuerySet": ...
    def distinct(self) -> "QuerySet": ...
    def annotate(self, **kwargs: Any) -> "QuerySet": ...
    def values_list(self, *fields_: str, flat: bool=...) -> "ValuesListQuery": ...
    def values(self, *args: str, **kwargs: str) -> "ValuesQuery": ...
    def delete(self) -> "DeleteQuery": ...
    def update(self, **kwargs: Any) -> "UpdateQuery": ...
    def count(self) -> "CountQuery": ...
    def all(self) -> "QuerySet": ...
    def first(self) -> "QuerySet": ...
    def get(self, *args: Any, **kwargs: Any) -> "QuerySet": ...
    def prefetch_related(self, *args: str) -> "QuerySet": ...
    async def explain(self) -> Any: ...
    def using_db(self, _db: BaseDBAsyncClient) -> "QuerySet": ...
    def __await__(self): ...
    def __aiter__(self) -> QueryAsyncIterator: ...

class UpdateQuery(AwaitableQuery):
    update_kwargs: Any = ...
    q_objects: Any = ...
    annotations: Any = ...
    custom_filters: Any = ...
    def __init__(self, model: Any, update_kwargs: Any, db: Any, q_objects: Any, annotations: Any, custom_filters: Any) -> None: ...

class DeleteQuery(AwaitableQuery):
    q_objects: Any = ...
    annotations: Any = ...
    custom_filters: Any = ...
    def __init__(self, model: Any, db: Any, q_objects: Any, annotations: Any, custom_filters: Any) -> None: ...

class CountQuery(AwaitableQuery):
    q_objects: Any = ...
    annotations: Any = ...
    custom_filters: Any = ...
    def __init__(self, model: Any, db: Any, q_objects: Any, annotations: Any, custom_filters: Any) -> None: ...

class FieldSelectQuery(AwaitableQuery):
    query: Any = ...
    def add_field_to_select_query(self, field: Any, return_as: Any) -> None: ...
    def resolve_to_python_value(self, model: Any, field: Any): ...

class ValuesListQuery(FieldSelectQuery):
    fields: Any = ...
    limit: Any = ...
    offset: Any = ...
    distinct: Any = ...
    orderings: Any = ...
    annotations: Any = ...
    custom_filters: Any = ...
    q_objects: Any = ...
    fields_for_select_list: Any = ...
    flat: Any = ...
    def __init__(self, model: Any, db: Any, q_objects: Any, fields_for_select_list: Any, limit: Any, offset: Any, distinct: Any, orderings: Any, flat: Any, annotations: Any, custom_filters: Any) -> None: ...

class ValuesQuery(FieldSelectQuery):
    fields_for_select: Any = ...
    limit: Any = ...
    offset: Any = ...
    distinct: Any = ...
    orderings: Any = ...
    annotations: Any = ...
    custom_filters: Any = ...
    q_objects: Any = ...
    def __init__(self, model: Any, db: Any, q_objects: Any, fields_for_select: Any, limit: Any, offset: Any, distinct: Any, orderings: Any, annotations: Any, custom_filters: Any) -> None: ...