from .GenericRequest import GenericRequest
from pykollib.pattern import PatternManager

from datetime import datetime


class ClanRaidLogRequest(GenericRequest):
    """
    This class retrieves a list of old raid logs that the clan has completed. In addition, it also
    returns information about any given raid instance.
    """

    def __init__(self, session, raidId=None):
        super(ClanRaidLogRequest, self).__init__(session)
        self.url = session.serverURL + "clan_raidlogs.php"
        self.raidId = raidId
        if raidId:
            self.url += "?viewlog=%s" % raidId

    def parseResponse(self):
        # If this is a request for a particular raid log, only retrieve information about it.
        txt = self.responseText
        if self.raidId:
            index = txt.find("<b>Current Clan Dungeons:</b>")
            if index > 0:
                txt = txt[:index]

        # Get a list of actions that occurred in Hobopolis.
        actions = []
        dungeonLogTypePattern = PatternManager.getOrCompilePattern("dungeonLogType")
        dungeonLogCategoryPattern = PatternManager.getOrCompilePattern(
            "dungeonLogCategory"
        )
        dungeonActivityPattern = PatternManager.getOrCompilePattern("dungeonActivity")
        for typeMatch in dungeonLogTypePattern.finditer(txt):
            dungeon = typeMatch.group(1)
            raidId = int(typeMatch.group(2))
            for categoryMatch in dungeonLogCategoryPattern.finditer(typeMatch.group(3)):
                category = categoryMatch.group(1)
                for match in dungeonActivityPattern.finditer(categoryMatch.group(2)):
                    action = {
                        "dungeon": dungeon,
                        "raidId": raidId,
                        "category": category,
                        "userName": match.group(1),
                        "userId": int(match.group(2)),
                        "event": match.group(3),
                        "turns": int(match.group(4).replace(",", "")),
                    }
                    actions.append(action)
        self.responseData["events"] = actions

        # Retrieve a list of loot that has been distributed.
        lootDistributed = []
        dungeonLootDistributionPattern = PatternManager.getOrCompilePattern(
            "dungeonLootDistribution"
        )
        for match in dungeonLootDistributionPattern.finditer(txt):
            m = {}
            m["distributorName"] = match.group(1)
            m["distributorId"] = int(match.group(2))
            m["itemName"] = match.group(3)
            m["receiverName"] = match.group(4)
            m["receiverId"] = match.group(5)
            lootDistributed.append(m)
        self.responseData["lootDistributed"] = lootDistributed

        # Retrieve a list of previous, completed runs.
        previousRuns = []
        dungeonPreviousRunPattern = PatternManager.getOrCompilePattern(
            "dungeonPreviousRun"
        )
        for match in dungeonPreviousRunPattern.finditer(self.responseText):
            run = {}

            # Parse the start date.
            dateStr = match.group(1)
            try:
                date = datetime.strptime(dateStr, "%B %d, %Y")
            except ValueError:
                date = dateStr
            run["startDate"] = date

            # Parse the end date.
            dateStr = match.group(2)
            try:
                date = datetime.strptime(dateStr, "%B %d, %Y")
            except ValueError:
                date = dateStr
            run["endDate"] = date

            # Get the remaining information.
            run["dungeonName"] = match.group(3)
            run["turns"] = int(match.group(4).replace(",", ""))
            run["id"] = int(match.group(5).replace(",", ""))
            previousRuns.append(run)
        self.responseData["previousRuns"] = previousRuns
