from . import Item

from dataclasses import dataclass
@dataclass
class ItemQuantity:
    item: "Item"
    quantity: int
