import re
from enum import Enum
from typing import List, NamedTuple

import libkol

from ..Error import UnknownError
from ..types import ItemQuantity
from ..Item import Item
from .request import Request

item_pattern = re.compile(
    r"<tr><td><img onclick\='descitem\((?P<itemdescid>[0-9]+)\).*?<b>(?P<itemname>.*?)\((?P<quantity>[0-9,]+])\)</td>'",
    re.DOTALL,
)

message_pattern = re.compile(
    r"<table cellpadding=5><tr><td.*?><b>Note:</b><Br><?/?c?e?n?t?e?r?>?(?P<message>.*?)</td></tr></table>",
    re.DOTALL,
)

incoming_response_pattern = re.compile(
    r'You will give (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\):<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+)<br><hr>.*? will give you:<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action\=accept&pwd\=.*?&whichoffer\=(?P<tradeid>[0-9]+)">accept',
    re.DOTALL,
)

outgoing_response_pattern = re.compile(
    r'You will give [^()]*?:<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+?)<br><hr>(?P<playername>.*?) \(#(?P<playerid>[0-9]+?)\) will give you:<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action=cancel2&whichoffer=(?P<tradeid>[0-9]+?)">cancel',
    re.DOTALL,
)

incoming_pattern = re.compile(
    r'Offer from (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\)<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="counteroffer\.php\?whichoffer=(?P<tradeid>[0-9]+)">respond',
    re.DOTALL,
)

outgoing_pattern = re.compile(
    r'Offered to (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\)<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action=cancel&whichoffer=(?P<tradeid>[0-9]+)">cancel this offer',
    re.DOTALL,
)


class Status(Enum):
    Incoming = 1
    Outgoing = 2
    IncomingResponse = 3
    OutgoingResponse = 4


class Trade(NamedTuple):
    id: int  # The ID of the trade.
    status: Status  # The status of the trade
    user_id: int  # The ID of the other player involved in this trade.
    username: str  # The name of the other player involved in this trade.
    incoming_items: List[
        ItemQuantity
    ]  # An array of items being offered to you in the format of a dictionary with keys itemID, quantity, and itemName.
    outgoing_items: List[
        ItemQuantity
    ]  # An array of items being offered to the other player in the format of a dictionary with keys itemID, quantity, and itemName.
    incoming_meat: int  # The amount of meat being offered by the other player.
    outgoing_meat: int  # The amount of meat being offered to the other player.
    message: str  # The message or note attached to the trade.


class trade_pending(Request[List[Trade]]):
    def __init__(self, session: "libkol.Session") -> None:
        self.request = session.request("makeoffer.php")

    @staticmethod
    async def parse_trade_items(content: str) -> List[ItemQuantity]:
        if content is None:
            return []

        return [
            ItemQuantity(item, quantity)
            for item, quantity in (
                (
                    (await Item.get_or_discover(desc_id=int(i.group("itemdescid")))),
                    int(i.group("quantity")),
                )
                for i in item_pattern.finditer(content)
            )
            if item is not None
        ]

    @classmethod
    async def parser(cls, content: str, **kwargs) -> List[Trade]:
        """
        Parse each different kind of trade.
        """
        statuses = [
            (Status.Incoming, incoming_pattern.finditer(content)),
            (Status.Outgoing, outgoing_pattern.finditer(content)),
            (Status.IncomingResponse, incoming_response_pattern.finditer(content)),
            (Status.OutgoingResponse, outgoing_response_pattern.finditer(content)),
        ]

        trades = []  # type: List[Trade]

        for status, match_group in statuses:
            for trade in match_group:
                results = trade.groupdict()

                message = results["message"]
                if message is not None:
                    match = message_pattern.search(message)

                    if match is None:
                        raise UnknownError("Failed to parse existing trade note")

                    message = match.group("message")

                trades += [
                    Trade(
                        id=int(results["tradeid"]),
                        status=status,
                        user_id=int(results["playerid"]),
                        username=results["playername"],
                        incoming_items=(
                            await cls.parse_trade_items(results["incomingitems"])
                        ),
                        outgoing_items=(
                            await cls.parse_trade_items(results["outgoingitems"])
                        ),
                        incoming_meat=(
                            int(results["incomingmeat"])
                            if results["incomingmeat"]
                            else 0
                        ),
                        outgoing_meat=(
                            int(results["outgoingmeat"])
                            if results["outgoingmeat"]
                            else 0
                        ),
                        message=message,
                    )
                ]

        return trades
