import re
from datetime import datetime
from html import unescape
from typing import List, NamedTuple

import libkol

from ..Error import UnknownError
from ..types import ItemQuantity
from ..pattern import PatternManager
from ..util import parsing
from .request import Request

full_message_pattern = re.compile(
    '<tr><td[^>]*><input type=checkbox name="sel([0-9]+)".*?<b>[^<]*<\/b> <a href="showplayer\.php\?who=([0-9]+)">([^<]*)<\/a>.*?<b>Date:<\/b>([^<]*?)</b>.*?<blockquote>(.*?)<\/blockquote>',
    re.DOTALL,
)

whitespace_pattern = PatternManager.getOrCompilePattern("whitespace")


class Message(NamedTuple):
    id: int  # The integer identifier for the message.
    user_id: int  # The ID of the user who sent or received this message.
    username: str  # The name of the user who sent or received this message.
    date: datetime  # The date the message was sent.
    text: str  # The contents of the message.
    items: List[ItemQuantity]  # Items attached to the message.
    meat: int  # The amount of meat sent with the message.
    type: str  # Type of message (coffee, candy, normal etc)


class kmail_get(Request):
    def __init__(
        self,
        session: "libkol.Session",
        box: str = "Inbox",
        page: int = 0,
        messages_per_page: int = 100,
        oldest_first: bool = False,
    ) -> None:
        """
        This request gets a list of kmails from the server.

        Due to a bug in KoL,
        it is highly recommended that you do not specify more than one
        of `page`, `messages_per_page`, and `oldest_first` in the same
        request. Doing so can cause the server to take up to 5 minutes
        to respond to your request. For now, if you want to specify two
        or three of these parameters, you should specify one at a time
        and make multiple requests. KoL is nice enough to remember the
        values you last used for both `messages_per_page` and `oldest_first`.
        """
        super().__init__(session)

        if messages_per_page not in [10, 20, 50, 100]:
            raise ValueError("messages_per_page can only be 10, 20, 50 or 100")

        params = {
            "box": box,
            "begin": str(page),
            "order": 1 if oldest_first else 0,
            "per_page": messages_per_page / 10,
        }

        self.request = session.request("messages.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Message]:
        """
        Parses through the response and constructs an array of messages.
        """

        messages = []  # type: List[Message]

        for message in full_message_pattern.finditer(content):
            messageId = int(message.group(1))
            userId = int(message.group(2))
            userName = message.group(3).strip()

            dateStr = message.group(4).strip()

            try:
                date = datetime.strptime(dateStr, "%A, %B %d, %Y, %I:%M%p")
            except ValueError:
                raise UnknownError("Found a date that we couldn't parse in a kmail")

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

            # Handle special messages.
            if "brokewin.gif" in content or "bigbrick.gif" in content:
                type = "brick"
            elif "/heart/cuptop.gif" in content:
                type = "coffeeCup"
            elif "/heart/hearttop.gif" in content:
                type = "candyHeart"
            else:
                type = "normal"

            messages += [
                Message(
                    id=messageId,
                    user_id=userId,
                    username=userName,
                    date=date,
                    text=text,
                    items=await parsing.item(rawText),
                    meat=parsing.meat(rawText),
                    type=type,
                )
            ]

        return messages
