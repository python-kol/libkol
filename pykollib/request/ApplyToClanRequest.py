from .GenericRequest import GenericRequest


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
            accepted: boolean
            alreadyMember: boolean
        """

        accepted = self.searchNamedPattern("clanApplicationAccepted")
        alreadyMember = self.searchNamedPattern("clanApplicationAlreadyMember")

        self.response = {
            "success": accepted or alreadyMember,
            "alreadyMember": alreadyMember,
        }
