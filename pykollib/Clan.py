from .request import ApplyToClanRequest, ClanRaidLogRequest, SearchClansRequest

class Clan(object):
    "This class represents a Clan in the Kingdom of Loathing"

    def __init__(self, session, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Must specify a name or id for a clan")

        self.session = session
        self.id = id
        self.name = name

        if id is None:
            searchResponse = SearchClansRequest(session, self.name, exact=True).doRequest()
            result = searchResponse["results"]
            if len(result) == 0:
                raise ValueError("Clan {} does not exist".format(self.name))
            self.id = result[0]["id"]


    def join(self):
        s = self.session

        applyResponse = ApplyToClanRequest(s, self.id).doRequest()
        success = applyResponse.get("success")

        if success:
            session.clan = self

        return success


    def getRaidLogs(self, raidId=None):
        s = self.session
        raidLogResponse = ClanRaidLogRequest(s, raidId).doRequest()
        return raidLogResponse
