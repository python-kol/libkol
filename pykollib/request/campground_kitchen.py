from aiohttp import ClientResponse
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


class Response(NamedTuple):
    oven: bool
    range: bool
    chef: bool
    shaker: bool
    cocktail: bool
    bartender: bool
    sushi: bool


def parse(html: str, **kwargs) -> Response:
    response = {
        "oven": "You've got an E-Z Cook&trade; oven installed in your kitchen." in html,
        "shaker": "You've got a My First Shaker&trade; cocktailcrafting kit in your kitchen."
        in html,
        "chef": "He'll help you cook fancy dishes, and make it so cooking doesn't cost an Adventure!"
        in html,
        "bartender": "He'll help you mix up fancy cocktails, and make it so cocktailcrafting doesn't cost an Adventure!"
        in html,
        "sushi": "Your kitchen is equipped with a sushi-rolling mat." in html,
    }

    if "You've got a Dramatic&trade; range installed in your kitchen." in html:
        response["oven"] = True
        response["range"] = True

    if "You've got a Queue Du Coq cocktailcrafting kit in your kitchen." in html:
        response["shaker"] = True
        response["cocktail"] = True

    return Response(**response)


def campground_kitchen(session: "Session") -> ClientResponse:
    """
    Checks state of the kitchen. (Did you wash the dishes?)
    """

    params = {"action": "inspectkitchen"}
    return session.request("campground.php", pwd=True, params=params, parse=parse)
