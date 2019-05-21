import re
from aiohttp import ClientResponse
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple, List

if TYPE_CHECKING:
    from ..Session import Session

from ..Item import Item, ItemQuantity

item_pattern = re.compile(
    r"<tr><td><img onclick\='descitem\((?P<itemdescid>[0-9]+)\).*?<b>(?P<itemname>.*?)\((?P<quantity>[0-9,]+])\)</td>'",
    re.DOTALL,
)

message_pattern = re.compile(
    r"<table cellpadding=5><tr><td.*?><b>Note:</b><Br><?/?c?e?n?t?e?r?>?(?P<message>.*?)</td></tr></table>",
    re.DOTALL,
)

incoming_response_pattern = re.compile(
    ': (r\'You will give (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\):<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+)<br><hr>.*? will give you:<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action\=accept&pwd\=.*?&whichoffer\=(?P<tradeid>[0-9]+)">accept',
    re.DOTALL,
)

outgoing_response_pattern = re.compile(
    r'You will give [^()]*?:<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+?)<br><hr>(?P<playername>.*?) \(#(?P<playerid>[0-9]+?)\) will give you:<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action=cancel2&whichoffer=(?P<tradeid>[0-9]+?)">cancel',
    re.DOTALL,
)

incoming_pattern = (
    (
        r'Offer from (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\)<br><table>(?P<incomingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<incomingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="counteroffer\.php\?whichoffer=(?P<tradeid>[0-9]+)">respond',
        re.DOTALL,
    ),
)

outgoing_pattern = (
    (
        r'Offered to (?P<playername>.*?) \(#(?P<playerid>[0-9]+)\)<br><table>(?P<outgoingitems>.*?)</table><img src="http://images\.kingdomofloathing\.com/itemimages/meat\.gif" width=30 height=30><b>:</b> (?P<outgoingmeat>[0-9,]+)<br>(?P<message>.*?)<a href="makeoffer\.php\?action=cancel&whichoffer=(?P<tradeid>[0-9]+)">cancel this offer',
        re.DOTALL,
    ),
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
        Item
    ]  # An array of items being offered to you in the format of a dictionary with keys itemID, quantity, and itemName.
    outgoing_items: List[
        Item
    ]  # An array of items being offered to the other player in the format of a dictionary with keys itemID, quantity, and itemName.
    incoming_meat: int  # The amount of meat being offered by the other player.
    outgoing_meat: int  # The amount of meat being offered to the other player.
    message: str  # The message or note attached to the trade.


def parse_trade_items(html: str) -> List[ItemQuantity]:
    if html is None:
        return []

    return [
        ItemQuantity(
            Item.get_or_none(desc_id=int(i.group("itemdescid"))),
            int(i.group("quantity")),
        )
        for i in item_pattern.finditer(html)
    ]


def parse(html: str, **kwargs) -> List[Trade]:
    """
    Parse each different kind of trade. Each trade offer or offer and response is represented as a dictionary with following keys:
    """
    statuses = [
        (Status.Incoming, incoming_pattern.finditer(html)),
        (Status.Outgoing, outgoing_pattern.finditer(html)),
        (Status.IncomingResponse, incoming_response_pattern.finditer(html)),
        (Status.OutgoingResponse, outgoing_response_pattern.finditer(html)),
    ]

    trades = []

    for status, match_group in statuses:
        for trade in match_group:
            results = trade.groupdict()

            message = results["message"]
            if message is not None:
                match = message_pattern.search(message)
                message = message.group("message") if match else None

            trades += [
                Trade(
                    **{
                        "id": int(results["tradeid"]),
                        "status": status,
                        "user_id": int(results["playerid"]),
                        "username": results["playername"],
                        "incoming_items": parse_trade_items(results["incomingitems"]),
                        "outgoing_items": parse_trade_items(results["outgoingitems"]),
                        "incoming_meat": int(results["incomingmeat"])
                        if results["incomingmeat"]
                        else 0,
                        "outgoing_meat": int(results["outgoingmeat"])
                        if results["outgoingmeat"]
                        else 0,
                        "message": message,
                    }
                )
            ]

    return trades


def trade_pending(session: "Session") -> ClientResponse:
    return session.request("makeoffer.php", parse=parse)
