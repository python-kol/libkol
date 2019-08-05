# Stubs for bs4 (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from .element import (
    Tag as Tag,
    PageElement as PageElement,
    Comment as Comment,
    NavigableString as NavigableString,
)
from typing import Any, Optional

class BeautifulSoup(Tag):
    ROOT_TAG_NAME: str = ...
    DEFAULT_BUILDER_FEATURES: Any = ...
    ASCII_SPACES: str = ...
    NO_PARSER_SPECIFIED_WARNING: str = ...
    builder: Any = ...
    is_xml: Any = ...
    known_xml: Any = ...
    parse_only: Any = ...
    markup: Any = ...
    def __init__(self, markup: str = ..., features: Optional[Any] = ..., builder: Optional[Any] = ..., parse_only: Optional[Any] = ..., from_encoding: Optional[Any] = ..., exclude_encodings: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def __copy__(self): ...
    hidden: bool = ...
    current_data: Any = ...
    currentTag: Any = ...
    tagStack: Any = ...
    preserve_whitespace_tag_stack: Any = ...
    def reset(self) -> None: ...
    def new_tag(self, name: Any, namespace: Optional[Any] = ..., nsprefix: Optional[Any] = ..., attrs: Any = ..., **kwattrs: Any): ...
    def new_string(self, s: Any, subclass: Any = ...): ...
    def popTag(self): ...
    def pushTag(self, tag: Any) -> None: ...
    def endData(self, containerClass: Any = ...) -> None: ...
    def object_was_parsed(self, o: Any, parent: Optional[Any] = ..., most_recent_element: Optional[Any] = ...) -> None: ...
    def handle_starttag(self, name: Any, namespace: Any, nsprefix: Any, attrs: Any): ...
    def handle_endtag(self, name: Any, nsprefix: Optional[Any] = ...) -> None: ...
    def handle_data(self, data: Any) -> None: ...

class BeautifulStoneSoup(BeautifulSoup):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class StopParsing(Exception): ...
class FeatureNotFound(ValueError): ...
