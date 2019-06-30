from typing import Optional
from dataclasses import dataclass

import libkol


@dataclass
class ItemQuantity:
    item: "libkol.Item"
    quantity: int


@dataclass
class Listing:
    item: Optional["libkol.Item"] = None
    price: int = 0
    stock: int = 0
    limit: int = 0
    limit_reached: bool = False
    store_id: Optional[int] = None
    store_name: Optional[str] = None


@dataclass
class FamiliarState:
    familiar: "libkol.Familiar"
    weight: int
    nickname: str
    experience: int = 0
    kills: int = 0
