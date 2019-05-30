from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def parse(json, **kwargs):
    return {
        "descId": int(json["descid"]),
        "name": json["name"],
        "plural": json["plural"]
        if "plural" in json and len(json["plural"]) > 0
        else None,
        "image": "%s.gif" % json["picture"]
        if "picture" in json and len(json["picture"]) > 0
        else None,
        "type": json["type"] if "type" in json else None,
        "autosell": int(json["sellvalue"])
        if "sellvalue" in json and int(json["sellvalue"] > 0)
        else 0,
        "power": int(json["power"]) if "power" in json else 0,
        "numHands": int(json["hands"])
        if "hands" in json and int(json["hands"] > 0)
        else 0,
        "canTransfer": True
        if "cantransfer" in json and json["cantransfer"] == "1"
        else False,
        "isCookingIngredient": True
        if "cook" in json and json["cook"] == "1"
        else False,
        "isCocktailcraftingIngredient": True
        if "cocktail" in json and json["cocktail"] == "1"
        else False,
        "isJewelrymakingComponent": True
        if "jewelry" in json and json["jewelry"] == "1"
        else False,
        "isMeatsmithingComponent": True
        if "smith" in json and json["smith"] == "1"
        else False,
        "isMeatpastingComponent": True
        if "combine" in json and json["combine"] == "1"
        else False,
        "isFancy": True if "fancy" in json and json["fancy"] == "1" else False,
        "isQuestItem": True if "quest" in json and json["quest"] == "1" else False,
        "isDiscardable": True
        if "candiscard" in json and json["candiscard"] == "1"
        else False,
        "isHardcoreDenied": True
        if "unhardcore" in json and json["unhardcore"] == "1"
        else False,
    }


def item_information(session: "pykollib.Session", item_id) -> Coroutine[Any, Any, ClientResponse]:
    "This class is used to get information about a particular item."

    data = {"what": "item", "id": item_id}
    return session.request("api.php", json=True, data=data, parse=parse)
