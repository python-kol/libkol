pykollib
=====

What is it?
-----------
The purpose of pykollib is to create a [Python](http://www.python.org/) package that makes it extremely easy to develop code that works with [The Kingdom of Loathing](http://www.kingdomofloathing.com). pykollib can be used for anything from writing short scripts to complex bots. In fact, both [kBay](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=141613) and [wadbot](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=152258) are built completely on top of it.

Who is it for?
--------------
pykollib is for programmers who are interested in writing scripts and bots for KoL. If you do not feel comfortable writing code, then pykollib is probably not for you.

Example
-------
The following is some example code that demonstrates how to login to The Kingdom of Loathing, grab the contents of your inbox, and start listening to chat.

```python
from pykollib.Session import Session
from pykollib.request import GetMessagesRequest
from pykollib.request import GetChatMessagesRequest
from pykollib.request import OpenChatRequest
from time import sleep

s = Session()
s.login('myusername', 'mypassword')

r = GetMessagesRequest(s)
responseData = r.doRequest()
kmails = responseData["kmails"]
for kmail in kmails:
    print "Received kmail from %s (#%s)" % (kmail["userName"], kmail["userId"])
    print "Text: %s" % kmail["text"]
    print "Meat: %s" % kmail["meat"]
    for item in kmail["items"]:
        print "Item: %s (%s)" % (item["name"], item["quantity"])

lastRequestTimestamp = 0
lastChatTimestamps = {}
r = OpenChatRequest(s)
d = r.doRequest()
print d
currentChannel = d["currentChannel"]
print currentChannel

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
    print chats
    sleep(10)
```

Requirements
------------
pykollib requires Python 3.x.

To install third-party libraries

```console
$ pip install -r requirements.txt
```

Running the Unit Tests
----------------------
pykollib includes a [unittest](http://docs.python.org/2/library/unittest.html) suite, to showcase some of its functionality and to help ensure that new game changes don't break your existing code. Developers are strongly encouraged to add unit tests for new features that they create.

To run the test suite:

```console
$ python -m pykollib.test.TestAll [username] [password]
```

How can I contribute?
---------------------
1. [Fork](http://help.github.com/forking/) pykollib
2. Clone your fork - `git clone git@github.com:your_username/pykollib.git`
3. Add a remote to this repository - `git remote add upstream git://github.com/scelis/pykollib.git`
4. Fetch the current pykollib sources - `git fetch upstream`
5. Create a topic branch - `git checkout -b my_branch upstream/master`
6. Commit (or cherry-pick) your changes
7. Push your branch to github - `git push origin my_branch`
8. Create an [Issue](http://github.com/scelis/pykollib/issues) with a link to your branch
9. That's it!
