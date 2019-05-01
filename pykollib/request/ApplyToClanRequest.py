from .GenericRequest import GenericRequest
import pykollib.Error as Error


class ApplyToClanRequest(GenericRequest):
    def __init__(self, session, target_id):
        super(ApplyToClanRequest, self).__init__(session)
        self.url = session.serverURL + "showclan.php"

        self.requestData = {
            "recruiter": 1,
            "pwd": session.pwd,
            "whichclan": target_id,
            "action": "joinclan",
            "apply": "Apply+to+this+Clan",
            "confirm": "on",
        }

    def parseResponse(self):
        """
        Returns a dict with the following possible elements:
            success: boolean
            alreadyMember: boolean
        """

        if self.searchNamedPattern("clanApplicationLeaderExisting"):
            raise Error.Error(
                "Cannot apply to another clan because you are the leader of {}".format(
                    self.session.preferences["clanName"]
                ),
                Error.CANNOT_CHANGE_CLAN,
            )

        accepted = self.searchNamedPattern("clanApplicationAccepted")
        alreadyMember = self.searchNamedPattern("clanApplicationAlreadyMember")

        self.responseData = {
            "success": accepted or alreadyMember,
            "alreadyMember": alreadyMember,
        }
