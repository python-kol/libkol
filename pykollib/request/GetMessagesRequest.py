from aiohttp import ClientResponse
from datetime import datetime
from typing import List, Dict, Any, TYPE_CHECKING
from html import unescape

from pykollib.database import ItemDatabase
from pykollib.pattern import PatternManager

if TYPE_CHECKING:
    from ..Session import Session

fullMessagePattern = PatternManager.getOrCompilePattern("fullMessage")
whitespacePattern = PatternManager.getOrCompilePattern("whitespace")
singleItemPattern = PatternManager.getOrCompilePattern("acquireSingleItem")
multiItemPattern = PatternManager.getOrCompilePattern("acquireMultipleItems")
meatPattern = PatternManager.getOrCompilePattern("gainMeat")
brickPattern = PatternManager.getOrCompilePattern("brickMessage")
coffeePattern = PatternManager.getOrCompilePattern("coffeeMessage")
candyHeartPattern = PatternManager.getOrCompilePattern("candyHeartMessage")


def parse(session: "Session", html: str, **kwargs) -> List[Dict[str, Any]]:
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

    for message in fullMessagePattern.finditer(html):
        messageId = int(message.group(1))
        userId = int(message.group(2))
        userName = message.group(3).strip()

        dateStr = message.group(4).strip()
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
        text = whitespacePattern.sub(" ", text)
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
        items = []
        for match in singleItemPattern.finditer(rawText):
            descId = int(match.group(1))
            item = ItemDatabase.getOrDiscoverItemFromDescId(descId, session)
            item["quantity"] = 1
            items.append(item)
        for match in multiItemPattern.finditer(rawText):
            descId = int(match.group(1))
            quantity = int(match.group(2).replace(",", ""))
            item = ItemDatabase.getOrDiscoverItemFromDescId(descId, session)
            item["quantity"] = quantity
            items.append(item)
        m["items"] = items

        # Find how much meat was attached to the message.
        meat = 0
        meatMatch = meatPattern.search(rawText)
        if meatMatch:
            meat = int(meatMatch.group(1).replace(",", ""))
        m["meat"] = meat

        # Handle special messages.
        if brickPattern.search(rawText):
            m["messageType"] = "brick"
        elif coffeePattern.search(rawText):
            m["messageType"] = "coffeeCup"
        elif candyHeartPattern.search(rawText):
            m["messageType"] = "candyHeart"
        else:
            m["messageType"] = "normal"

        messages.append(m)

    return messages


def getMessagesRequest(
    session: "Session",
    box: str = "Inbox",
    page: int = 0,
    messages_per_page: int = None,
    oldest_first: bool = False,
) -> ClientResponse:
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
    params = {"box": box}
    if page > 1:
        params["begin"] = page

    if messages_per_page:
        if messages_per_page not in [10, 20, 50, 100]:
            raise ValueError("messages_per_page can only be 10, 20, 50 or 100")

        params["per_page"] = messages_per_page / 10

    if oldest_first:
        params["order"] = 1

    return session.request("messages.php", params=params, parse=parse)
