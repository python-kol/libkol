"""
This example demonstrates how to login to The Kingdom of Loathing,
grab the contents of your inbox, and start listening to chat.
"""

import os
from dotenv import load_dotenv
from libkol import run, Session
from libkol.request import chat_channel

load_dotenv()


async def main():
    async with Session() as kol:
        await kol.login(os.getenv("KOL_USERNAME"), os.getenv("KOL_PASSWORD"))

        kmails = await kol.kmail.get()
        for kmail in kmails:
            print(f"Received kmail from {kmail.username} (#{kmail.user_id})")
            print(f"Text: {kmail.text}")
            print(f"Meat: {kmail.meat}")
            for iq in kmail.items:
                print(f"Item: {iq.item.name} ({iq.quantity})")

        current_channel = await chat_channel(kol).parse()
        print(current_channel)

        async for messages in kol.chat.messages():
            print(messages)


if __name__ == "__main__":
    run(main)
