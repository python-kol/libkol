from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import EffectNotFoundError, ItemNotFoundError, UnknownError


def parse(html: str, **kwargs) -> bool:
    if "<td>You don't have that effect." in html:
        raise EffectNotFoundError(
            "Unable to remove effect. The user does not have that effect."
        )

    if "<td>You don't have a green soft eyedrop echo antidote." in html:
        raise ItemNotFoundError(
            "Unable to remove effect. You do not have a soft green echo eyedrop antidote."
        )

    if "<td>Effect removed.</td>" not in html:
        raise UnknownError("Unable to remove effect")

    return True


def uneffect(session: "Session", effect_id: int) -> ClientResponse:
    params = {"using": "Yep.", "whicheffect": effect_id}

    return session.request("uneffect.php", pwd=True, params=params, parse=parse)
