import pykollib.Error as Error
from .GenericRequest import GenericRequest
from pykollib.pattern import PatternManager
from pykollib.util import parsing


class EatFoodRequest(GenericRequest):
    """
    This class is for eating food from the inventory.
    It accepts the current session and the ID number of the food to eat.
    It returns the results, including and stat gain, adventure gain, or effect gain.
    """

    def __init__(self, session, foodId):
        super(EatFoodRequest, self).__init__(session)
        self.url = (
            session.server_url
            + "inv_eat.php?pwd="
            + session.pwd
            + "&which=1&whichitem="
            + str(foodId)
        )

    def parseResponse(self):
        # Check for errors
        tooFullPattern = PatternManager.getOrCompilePattern("tooFull")
        if tooFullPattern.search(self.responseText):
            raise Error.Error("You are too full to eat that.", Error.USER_IS_FULL)
        notFoodPattern = PatternManager.getOrCompilePattern("notFood")
        if notFoodPattern.search(self.responseText):
            raise Error.Error("That item is not food.", Error.WRONG_KIND_OF_ITEM)
        foodMissingPattern = PatternManager.getOrCompilePattern("notEnoughItems")
        if foodMissingPattern.search(self.responseText):
            raise Error.Error("Item not in inventory.", Error.ITEM_NOT_FOUND)

        # Check the results
        results = {}
        results["adventures"] = parsing.adventures(self.responseText)

        substats = parsing.substat(self.responseText)
        if len(substats) > 0:
            results["substats"] = substats
        stats = parsing.stat(self.responseText)
        if len(stats) > 0:
            results["stats"] = stats
        level = parsing.level(self.responseText)
        if level != 0:
            results["level"] = level
        hp = parsing.hp(self.responseText)
        if hp != 0:
            results["hp"] = hp
        mp = parsing.mp(self.responseText)
        if mp != 0:
            results["mp"] = mp
        effects = parsing.effects(self.responseText)
        if len(effects) > 0:
            results["effects"] = effects

        self.responseData = results
