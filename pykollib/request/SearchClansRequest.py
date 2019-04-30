from .GenericRequest import GenericRequest


class SearchClansRequest(GenericRequest):
    def __init__(self, session, query, exact=False, nameonly=True):
        super(SearchClansRequest, self).__init__(session)
        self.url = session.serverURL + "clan_signup.php"

        self.query = query
        self.exact = exact

        self.requestData = {
            "action": "search",
            "searchstring": query,
            "whichfield": 1 if nameonly else 0,
            "countoper": 0,
            "countqty": 0,
            "furn1": 0,
            "furn2": 0,
            "furn3": 0,
            "furn4": 0,
            "furn5": 0,
            "furn9": 0,
        }

    def parseResponse(self):
        results = []
        resultPattern = self.getPattern("clanSearchResult")

        for resultMatch in resultPattern.finditer(self.responseText):
            result = {"id": int(resultMatch.group(1)), "name": resultMatch.group(2)}
            results.append(result)
            if self.exact:
                if result["name"].lower() != self.query.lower():
                    results = []
                break

        self.responseData = {"results": results}
