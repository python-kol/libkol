from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report
import kol.Error as Error

class DeclineTradeResponseRequest(GenericRequest):
    
    def __init__(self, session, tradeid):
        super(DeclineTradeResponseRequest, self).__init__(session)
        self.url = session.serverURL + 'makeoffer.php'
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'decline2'
        self.requestData['whichoffer'] = tradeid
    
    def parseResponse(self):
        successPattern = PatternManager.getOrCompilePattern('tradeCancelledSuccessfully')
        if successPattern.search(self.responseText):
            Report.trace('request', "Trade response " + str(self.requestData['whichoffer']) + " cancelled successfully.")
        else:
            raise Error.Error("Unknown error declining trade response for trade " + str(self.requestData['whichoffer']), Error.REQUEST_GENERIC)