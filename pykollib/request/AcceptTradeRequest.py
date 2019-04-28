from pykollib.request.GenericRequest import GenericRequest
from pykollib.manager import PatternManager
from pykollib.util import Report
import pykollib.Error as Error

class AcceptTradeRequest(GenericRequest):
    
    def __init__(self, session, tradeid):
        super(AcceptTradeRequest, self).__init__(session)
        self.url = session.serverURL + 'makeoffer.php'
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'accept'
        self.requestData['whichoffer'] = tradeid
    
    def parseResponse(self):
        successPattern = PatternManager.getOrCompilePattern('tradeAccepted')
        if successPattern.search(self.responseText):
            Report.trace('request', "Trade " + str(self.requestData['whichoffer']) "accepted successfully.")
        else:
            raise Error.Error("Unknown error accepted trade " + str(self.requestData['whichoffer']), Error.REQUEST_GENERIC)
