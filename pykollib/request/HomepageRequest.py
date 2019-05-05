from urllib.parse import urlparse
from aiohttp import ClientResponse

from ..Error import LoginFailedGenericError

from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


async def parse(url: str, **kwargs) -> Dict[str, Any]:
    return {"server_url": str(url.origin())}


async def homepageRequest(session: "Session", server_number: int = 0) -> ClientResponse:
    """
    This request is most often used before logging in. It allows the KoL servers to assign a
    particular server number to the user. In addition, it gives us the user's login challenge
    so that we might login to the server in a more secure fashion.
    """
    if server_number > 0:
        url = "https://www{}.kingdomofloathing.com/main.php".format(server_number)
    else:
        url = "https://www.kingdomofloathing.com/"

    return await session.post(url, parse=parse)
