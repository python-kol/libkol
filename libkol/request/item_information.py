from typing import Any, Dict, NamedTuple, Optional

import libkol

from .request import Request


class Response(NamedTuple):
    descid: int
    name: str
    plural: Optional[str]
    image: Optional[str]
    type: Optional[str]
    autosell: int
    power: int
    num_hands: int
    can_transfer: bool
    is_cooking_ingredient: bool
    is_cocktailcrafting_ingredient: bool
    is_jewelrymaking_component: bool
    is_meatsmithing_component: bool
    is_meatpasting_component: bool
    is_fancy: bool
    is_quest_item: bool
    is_discardable: bool
    is_hardcore_denied: bool


class item_information(Request):
    """
    Get information about a particular item.
    """

    def __init__(self, session: "libkol.Session", item_id) -> None:
        super().__init__(session)

        data = {"what": "item", "id": item_id}
        self.request = session.request("api.php", json=True, data=data)

    @staticmethod
    async def parser(json: Dict[str, Any], **kwargs) -> Response:
        return Response(
            descid=int(json["descid"]),
            name=json["name"],
            plural=(
                json["plural"] if "plural" in json and len(json["plural"]) > 0 else None
            ),
            image=(
                "{}.gif".format(json["picture"])
                if "picture" in json and len(json["picture"]) > 0
                else None
            ),
            type=json["type"] if "type" in json else None,
            autosell=(
                int(json["sellvalue"])
                if "sellvalue" in json and int(json["sellvalue"] > 0)
                else 0
            ),
            power=int(json["power"]) if "power" in json else 0,
            num_hands=(
                int(json["hands"]) if "hands" in json and int(json["hands"] > 0) else 0
            ),
            can_transfer=(
                True if "cantransfer" in json and json["cantransfer"] == "1" else False
            ),
            is_cooking_ingredient=(
                True if "cook" in json and json["cook"] == "1" else False
            ),
            is_cocktailcrafting_ingredient=(
                True if "cocktail" in json and json["cocktail"] == "1" else False
            ),
            is_jewelrymaking_component=(
                True if "jewelry" in json and json["jewelry"] == "1" else False
            ),
            is_meatsmithing_component=(
                True if "smith" in json and json["smith"] == "1" else False
            ),
            is_meatpasting_component=(
                True if "combine" in json and json["combine"] == "1" else False
            ),
            is_fancy=True if "fancy" in json and json["fancy"] == "1" else False,
            is_quest_item=True if "quest" in json and json["quest"] == "1" else False,
            is_discardable=(
                True if "candiscard" in json and json["candiscard"] == "1" else False
            ),
            is_hardcore_denied=(
                True if "unhardcore" in json and json["unhardcore"] == "1" else False
            ),
        )
