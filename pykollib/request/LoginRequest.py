import re
from aiohttp import ClientResponse
import hashlib

from ..Error import LoginFailedBadPasswordError, LoginFailedGenericError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

mainFrameset = re.compile(r'<frameset id="?rootset"?')
rateLimit = re.compile(r"wait (.+?) minutes?")
rateLimitIP = re.compile(r"Too many login failures from this IP")
badPassword = re.compile(r"<b>Login failed\.\s+?Bad password\.<\/b>")


def parse(html: str, **kwargs) -> bool:
    if mainFrameset.search(html):
        return True

    if badPassword.search(html):
        raise LoginFailedBadPasswordError("Login failed. Bad password.")

    match = rateLimit.search(html)
    if match:
        waits = {"a": 1, "a couple of": 2, "five": 5, "fifteen": 15}
        wait = waits.get(match.group(1), 1)
        raise LoginFailedGenericError(
            "Too many login attempts. Please wait {} minute(s) and try again.".format(
                wait
            ),
            wait=wait * 60,
        )

    if rateLimitIP.search(html):
        raise LoginFailedGenericError(
            "Too many login attempts from this IP. Please wait 15 minutes and try again.",
            wait=15 * 60,
        )

    raise LoginFailedGenericError("Unknown login error.")


def loginRequest(
    session: "Session",
    username: str,
    password: str,
    challenge: str = None,
    stealth: bool = False,
) -> ClientResponse:
    payload = {
        "loggingin": "Yup.",
        "loginname": username + (stealth and "/q"),
        "password": password,
        "secure": "1",
    }

    if challenge is not None:
        password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        response_key = "{}:{}".format(password_hash, challenge)
        response = hashlib.md5(response_key.encode("utf-8")).hexdigest()
        payload = {**payload, "challenge": challenge, "response": response}

    return session.request("login.php", data=payload, parse=parse)
