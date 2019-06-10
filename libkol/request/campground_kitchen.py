from typing import NamedTuple

import libkol

from .request import Request


class Response(NamedTuple):
    oven: bool
    range: bool
    chef: bool
    shaker: bool
    cocktail: bool
    bartender: bool
    sushi: bool


class campground_kitchen(Request[Response]):
    """
    Checks state of the kitchen. (Did you wash the dishes?)

    :param session: Active session
    """

    def __init__(self, session: "libkol.Session"):
        params = {"action": "inspectkitchen"}
        self.request = session.request("campground.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        response = {
            "oven": "You've got an E-Z Cook&trade; oven installed in your kitchen."
            in content,
            "shaker": "You've got a My First Shaker&trade; cocktailcrafting kit in your kitchen."
            in content,
            "chef": "He'll help you cook fancy dishes, and make it so cooking doesn't cost an Adventure!"
            in content,
            "bartender": "He'll help you mix up fancy cocktails, and make it so cocktailcrafting doesn't cost an Adventure!"
            in content,
            "sushi": "Your kitchen is equipped with a sushi-rolling mat." in content,
        }

        if "You've got a Dramatic&trade; range installed in your kitchen." in content:
            response["oven"] = True
            response["range"] = True

        if "You've got a Queue Du Coq cocktailcrafting kit in your kitchen." in content:
            response["shaker"] = True
            response["cocktail"] = True

        return Response(**response)
