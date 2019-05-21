import pykollib.Error as Error
from .GenericRequest import GenericRequest
from pykollib.pattern import PatternManager
from pykollib.util import parsing


class UseMultipleRequest(GenericRequest):
    "Uses multiple items at once"

    def __init__(self, session, item, quantity):
        super(UseMultipleRequest, self).__init__(session)
        self.url = session.server_url + "multiuse.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "useitem"
        self.requestData["quantity"] = quantity
        self.requestData["whichitem"] = item["id"]

        self.session = session

    def parseResponse(self):
        # First parse for errors
        notEnoughPattern = PatternManager.getOrCompilePattern("notEnoughToUse")
        if notEnoughPattern.search(self.responseText):
            raise Error.Error(
                "You don't have that many of that item.", Error.ITEM_NOT_FOUND
            )

        notMultiPattern = PatternManager.getOrCompilePattern("notMultiUse")
        if notMultiPattern.search(self.responseText):
            raise Error.Error(
                "You cannot multi-use that item.", Error.WRONG_KIND_OF_ITEM
            )

        # Find out what happened
        items = parsing.item(self.responseText)
        if len(items) > 0:
            self.responseData["items"] = items

        meat = parsing.meat(self.responseText)
        if meat != 0:
            self.responseData["meat"] = meat

        hp = parsing.hp(self.responseText)
        if hp != 0:
            self.responseData["hp"] = hp

        mp = parsing.mp(self.responseText)
        if mp != 0:
            self.responseData["mp"] = mp

        drunk = parsing.inebriety(self.responseText)
        if drunk != 0:
            self.responseData["drunk"] = drunk

        adventures = parsing.adventures(self.responseText)
        if adventures != 0:
            self.responseData["adventures"] = adventures

        effects = parsing.effects(self.responseText)
        if len(effects) > 0:
            self.responseData["effects"] = effects
