# Stubs for bs4.diagnose (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from html.parser import HTMLParser
from typing import Any

__license__: str

def diagnose(data: Any) -> None: ...
def lxml_trace(data: Any, html: bool = ..., **kwargs: Any) -> None: ...

class AnnouncingParser(HTMLParser):
    def handle_starttag(self, name: Any, attrs: Any) -> None: ...
    def handle_endtag(self, name: Any) -> None: ...
    def handle_data(self, data: Any) -> None: ...
    def handle_charref(self, name: Any) -> None: ...
    def handle_entityref(self, name: Any) -> None: ...
    def handle_comment(self, data: Any) -> None: ...
    def handle_decl(self, data: Any) -> None: ...
    def unknown_decl(self, data: Any) -> None: ...
    def handle_pi(self, data: Any) -> None: ...

def htmlparser_trace(data: Any) -> None: ...
def rword(length: int = ...): ...
def rsentence(length: int = ...): ...
def rdoc(num_elements: int = ...): ...
def benchmark_parsers(num_elements: int = ...) -> None: ...
def profile(num_elements: int = ..., parser: str = ...) -> None: ...