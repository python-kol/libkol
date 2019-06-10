from . import Item

from dataclasses import dataclass


@dataclass
class ItemQuantity:
    item: "Item"
    quantity: int


@dataclass
class Listing:
    item: Item
    price: int
    store_id: int
    store_name: str
    stock: int
    limit: int
    limit_reached: bool
