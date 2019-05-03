from . import GenericRequest
from ..pattern import PatternManager
from .. import Clan


class UserProfileRequest(GenericRequest):
    def __init__(self, session, playerId):
        super(UserProfileRequest, self).__init__(session)
        self.url = session.serverURL + "showplayer.php"
        self.requestData["who"] = playerId

    def parseResponse(self):
        usernameMatch = self.searchNamedPattern("profileUserName")
        ascensionsMatch = self.searchNamedPattern("profileNumAscensions")
        trophiesMatch = self.searchNamedPattern("profileNumTrophies")
        tattoosMatch = self.searchNamedPattern("profileNumTattoos")

        data = {
            "username": usernameMatch.group(1),
            "numAscensions": int(ascensionsMatch.group(1)) if ascensionsMatch else 0,
            "numTrophies": int(trophiesMatch.group(1)) if trophiesMatch else 0,
            "numTattoos": int(tattoosMatch.group(1)) if tattoosMatch else 0,
        }

        clanMatch = self.searchNamedPattern("profileClan")
        if clanMatch:
            data = {
                **data,
                "clanId": int(clanMatch.group(1)),
                "clanName": clanMatch.group(2),
            }
            self.session.clan = Clan.Clan(
                self, id=data["clanId"], name=data["clanName"]
            )

        self.preferences.setall(data)
        self.responseData = data
