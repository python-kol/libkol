from .request import (
    HomepageRequest,
    UserProfileRequest,
    LoginRequest,
    LogoutRequest,
    StatusRequest,
    CharpaneRequest,
)
from .util.Preferences import Preferences

import requests
import hashlib


class Session(object):
    "This class represents a user's session with The Kingdom of Loathing."

    def __init__(self):
        self.opener = requests.Session()
        self.preferences = Preferences("anonymous_prefs.db", False, True)
        self.isConnected = False
        self.userId = None
        self.userName = None
        self.userPasswordHash = None
        self.serverURL = None
        self.pwd = None
        self.clan = None

    def login(self, username, password, serverNumber=0):
        """
        Perform a KoL login given a username and password. A server number may also be specified
        to ensure that the user logs in using that particular server. This can be helpful
        if the user continues to be redirected to a server that is down.
        """

        self.userName = username
        self.userPasswordHash = hashlib.md5(password.encode("utf-8")).hexdigest()
        self.password = password

        # Load preferences for user
        self.preferences.load("{}_prefs.db".format(username), True)

        # Grab the KoL homepage.
        homepageResponse = HomepageRequest(self, serverNumber=serverNumber).doRequest()
        self.serverURL = homepageResponse["serverURL"]

        # Perform the login.
        loginRequest = LoginRequest(self, "")
        loginRequest.doRequest()

        # Load the charpane once to make StatusRequest report the rollover time
        charpaneRequest = CharpaneRequest(self)
        charpaneRequest.doRequest()

        self.getStatus()
        self.getProfile()

    def getUsername(self):
        return self.userName

    def getStatus(self):
        # Get pwd, user ID, and the user's name.
        request = StatusRequest(self)
        response = request.doRequest()

        self.pwd = response["pwd"]
        self.userName = response["name"]
        self.userId = int(response["playerid"])
        self.rollover = int(response["rollover"])

    def getProfile(self):
        return UserProfileRequest(self, self.userId).doRequest()

    def logout(self):
        "Performs a logut request, closing the session."
        LogoutRequest(self).doRequest()
