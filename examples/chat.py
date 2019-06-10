"""
This example demonstrates how to login to The Kingdom of Loathing, grab the contents of your inbox,
and start listening to chat.
"""

import asyncio
from libkol import Session
from libkol.request import getChatMessagesRequest, openChatRequest


async def main():
    async with Session() as kol:
        await kol.login("username", "password")

        kmails = await kol.kmail.get()
        for kmail in kmails:
            print("Received kmail from %s (#%s)" % (kmail["userName"], kmail["userId"]))
            print("Text: %s" % kmail["text"])
            print("Meat: %s" % kmail["meat"])
            for item in kmail["items"]:
                print("Item: %s (%s)" % (item["name"], item["quantity"]))

        lastRequestTimestamp = 0
        current_channel = (await (await openChatRequest(kol)).parse())[
            "current_channel"
        ]
        print(current_channel)

        while True:
            data = await (
                await getChatMessagesRequest(kol, lastRequestTimestamp)
            ).parse()
            lastRequestTimestamp = data["lastSeen"]
            chats = data["chatMessages"]

            # Set the channel in each channel-less chat to be the current channel.
            for chat in chats:
                t = chat["type"]
                if t == "normal" or t == "emote":
                    if "channel" not in chat:
                        chat["channel"] = current_channel
            print(chats)
            await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
