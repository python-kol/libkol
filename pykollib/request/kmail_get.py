import re
from datetime import datetime
from html import unescape
from typing import Any, Coroutine, Dict, List, Union

from aiohttp import ClientResponse

import pykollib

from ..pattern import PatternManager
from ..util import parsing

brick_message_pattern = re.compile(
    r"\/\/images\.kingdomofloathing\.com\/adventureimages\/(brokewin|bigbrick)\.gif"
)
candy_heart_message_pattern = re.compile(
    r"\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/hearttop\.gif"
)
coffee_message_pattern = re.compile(
    r"\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/cuptop\.gif"
)
full_message_pattern = re.compile(
    '<tr><td[^>]*><input type=checkbox name="sel([0-9]+)".*?<b>[^<]*<\/b> <a href="showplayer\.php\?who=([0-9]+)">([^<]*)<\/a>.*?<b>Date:<\/b>([^<]*?)</b>.*?<blockquote>(.*?)<\/blockquote>',
    re.DOTALL,
)

whitespace_pattern = PatternManager.getOrCompilePattern("whitespace")


def parse(session: "pykollib.Session", html: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Parses through the response and constructs an array of messages.
    Each message is represented as a dictionary with the following
    keys:

          id -- The integer identifier for the message.
      userId -- The ID of the user who sent or received this message.
    userName -- The name of the user who sent or received this message.
        date -- The date the message was sent as a datetime object.
        text -- The contents of the message.
       items -- An array of items attached to the message.
        meat -- The amount of meat sent with the message.
    """

    messages = []

    for message in full_message_pattern.finditer(html):
        messageId = int(message.group(1))
        userId = int(message.group(2))
        userName = message.group(3).strip()

        dateStr = message.group(4).strip()

        date = ""  # type: Union[datetime, str]
        try:
            date = datetime.strptime(dateStr, "%A, %B %d, %Y, %I:%M%p")
        except ValueError:
            date = dateStr

        rawText = message.group(5).strip()
        index = rawText.find("<center")
        if index >= 0:
            text = rawText[:index].strip()
        else:
            text = rawText.strip()

        # Get rid of extraneous spaces, tabs, or new lines.
        text = text.replace("\r\n", "\n")
        text = whitespace_pattern.sub(" ", text)
        text = text.replace("<br />\n", "\n")
        text = text.replace("<br/>\n", "\n")
        text = text.replace("<br>\n", "\n")
        text = text.replace("\n<br />", "\n")
        text = text.replace("\n<br/>", "\n")
        text = text.replace("\n<br>", "\n")
        text = text.replace("<br />", "\n")
        text = text.replace("<br/>", "\n")
        text = text.replace("<br>", "\n")
        text = text.strip()

        # KoL encodes all of the HTML entities in the message. Let's decode them to get the real text.
        text = unescape(text)

        m = {
            "id": messageId,
            "userId": userId,
            "userName": userName,
            "date": date,
            "text": text,
        }

        # Find the items attached to the message.
        m["items"] = parsing.item(rawText)

        # Find how much meat was attached to the message.
        m["meat"] = parsing.meat(rawText)

        # Handle special messages.
        if brick_message_pattern.search(rawText):
            m["messageType"] = "brick"
        elif coffee_message_pattern.search(rawText):
            m["messageType"] = "coffeeCup"
        elif candy_heart_message_pattern.search(rawText):
            m["messageType"] = "candyHeart"
        else:
            m["messageType"] = "normal"

        messages.append(m)

    return messages


def kmail_get(
    session: "pykollib.Session",
    box: str = "Inbox",
    page: int = 0,
    messages_per_page: int = 100,
    oldest_first: bool = False,
) -> Coroutine[Any, Any, ClientResponse]:
    """
    This request gets a list of kmails from the server.
    Due to a bug in KoL,
    it is highly recommended that you do not specify more than one
    of pageNumber, messagesPerPage, and oldestFirst in the same
    request. Doing so can cause the server to take up to 5 minutes
    to respond to your request. For now, if you want to specify two
    or three of these parameters, you should specify one at a time
    and make multiple requests. KoL is nice enough to remember the
    values you last used for both messagesPerPage and oldestFirst.
    """
    if messages_per_page not in [10, 20, 50, 100]:
        raise ValueError("messages_per_page can only be 10, 20, 50 or 100")

    params = {
        "box": box,
        "begin": str(page),
        "order": 1 if oldest_first else 0,
        "per_page": messages_per_page / 10,
    }

    return session.request("messages.php", params=params, parse=parse)
