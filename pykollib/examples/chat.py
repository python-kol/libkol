"""
This example demonstrates how to login to The Kingdom of Loathing, grab the contents of your inbox,
and start listening to chat.
"""
from pykollib.Session import Session
from pykollib.request import GetMessagesRequest
from pykollib.request import GetChatMessagesRequest
from pykollib.request import OpenChatRequest
from time import sleep

s = Session()
s.login("myusername", "mypassword")

r = GetMessagesRequest(s)
responseData = r.doRequest()
kmails = responseData["kmails"]
for kmail in kmails:
    print("Received kmail from %s (#%s)" % (kmail["userName"], kmail["userId"]))
    print("Text: %s" % kmail["text"])
    print("Meat: %s" % kmail["meat"])
    for item in kmail["items"]:
        print("Item: %s (%s)" % (item["name"], item["quantity"]))

lastRequestTimestamp = 0
lastChatTimestamps = {}
r = OpenChatRequest(s)
d = r.doRequest()
print(d)
currentChannel = d["currentChannel"]
print(currentChannel)

foo = True
while foo:
    c = GetChatMessagesRequest(s, lastRequestTimestamp)
    data = c.doRequest()
    lastRequestTimestamp = data["lastSeen"]
    chats = data["chatMessages"]

    # Set the channel in each channel-less chat to be the current channel.
    for chat in chats:
        t = chat["type"]
        if t == "normal" or t == "emote":
            if "channel" not in chat:
                chat["channel"] = currentChannel
    print(chats)
    sleep(10)
