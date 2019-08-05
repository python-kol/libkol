from typing import Any, Dict, Optional
from dataclasses import dataclass

import libkol

from .request import Request


@dataclass
class Response:
    descid: int
    name: str
    plural: Optional[str]
    image: Optional[str]
    type: Optional[str]
    autosell_value: int
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


class item_information(Request[Response]):
    """
    Get information about a particular item.
    """

    def __init__(self, session: "libkol.Session", item_id) -> None:
        super().__init__(session)

        data = {"what": "item", "id": item_id}
        self.request = session.request("api.php", json=True, data=data)

    @staticmethod
    async def parser(content: Dict[str, Any], **kwargs) -> Response:
        return Response(
            descid=int(content["descid"]),
            name=content["name"],
            plural=(
                content["plural"] if "plural" in content and len(content["plural"]) > 0 else None
            ),
            image=(
                "{}.gif".format(content["picture"])
                if "picture" in content and len(content["picture"]) > 0
                else None
            ),
            type=content["type"] if "type" in content else None,
            autosell_value=(
                int(content["sellvalue"])
                if "sellvalue" in content and int(content["sellvalue"] > 0)
                else 0
            ),
            power=int(content["power"]) if "power" in content else 0,
            num_hands=(
                int(content["hands"]) if "hands" in content and int(content["hands"] > 0) else 0
            ),
            can_transfer=(
                True if "cantransfer" in content and content["cantransfer"] == "1" else False
            ),
            is_cooking_ingredient=(
                True if "cook" in content and content["cook"] == "1" else False
            ),
            is_cocktailcrafting_ingredient=(
                True if "cocktail" in content and content["cocktail"] == "1" else False
            ),
            is_jewelrymaking_component=(
                True if "jewelry" in content and content["jewelry"] == "1" else False
            ),
            is_meatsmithing_component=(
                True if "smith" in content and content["smith"] == "1" else False
            ),
            is_meatpasting_component=(
                True if "combine" in content and content["combine"] == "1" else False
            ),
            is_fancy=True if "fancy" in content and content["fancy"] == "1" else False,
            is_quest_item=True if "quest" in content and content["quest"] == "1" else False,
            is_discardable=(
                True if "candiscard" in content and content["candiscard"] == "1" else False
            ),
            is_hardcore_denied=(
                True if "unhardcore" in content and content["unhardcore"] == "1" else False
            ),
        )
