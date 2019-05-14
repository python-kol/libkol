import pykollib.Error as Error
from pykollib.util import Report
from pykollib.pattern import PatternManager
from html.parser import HTMLParser


class GenericRequest(object):
    """
    A generic request to a Kingdom of Loathing server.  All specific KoL
    request classes should inherit from this class.  KoL request classes should
    also usually define a parseResponse() method of no arguments that returns
    a dict of data gleaned from the HTML of the KoL server's response.

    To use a request class that inherits GenericRequest:
        requestMaybeWithParams = SomeRequest(session[, param1, param2 ...])
        response = requestMaybeWithParams.doRequest()
    """

    HTML_PARSER = HTMLParser()

    def __init__(self, session):
        self.session = session
        self.server_url = session.server_url
        self.requestData = {}
        self.skipParseResponse = False

    async def doRequest(self):
        """
        Performs the request. This method will ensure that nightly maintenance
        is not occurring.  In addition, this method will throw a NOT_LOGGED_IN
        error if the session thinks it is logged in when it actually isn't.
        """

        Report.debug("request", "Requesting {0}".format(self.url))

        self.response = await self.session.request(self.url, data=self.requestData)
        self.responseText = await self.response.text()

        Report.debug("request", "Received response: {0}".format(self.url))
        Report.debug("request", "Response Text: {0}".format(self.responseText))

        if str(self.response.url).find("/maint.php") >= 0:
            self.session.is_connected = False
            raise Error.Error(
                "Nightly maintenance in progress.", Error.NIGHTLY_MAINTENANCE
            )

        if str(self.response.url).find("/login.php") >= 0:
            if self.session.is_connected:
                self.session.is_connected = False
                raise Error.Error(
                    "You are no longer connected to the server.", Error.NOT_LOGGED_IN
                )

        # Allow for classes that extend GenericRequest to parse all of the data someone
        # would need from the response and then to place this data in self.responseData.
        self.responseData = {}
        if self.skipParseResponse == False and hasattr(self, "parseResponse"):
            self.parseResponse()
            if len(self.responseData) > 0:
                Report.debug(
                    "request", "Parsed response data: {0}".format(self.responseData)
                )

        return self.responseData

    def getPattern(self, patternName):
        """
        Return a compiled re object for the given patternName.
        If one doesn't already exist, compile one and return it.
        """
        return PatternManager.getOrCompilePattern(patternName)

    def searchNamedPattern(self, patternName):
        """
        Search responseText for matches for the RE named by patternName.
        This is intended to be a useful shorthand in parseResponse() methods.
        """
        return self.getPattern(patternName).search(self.responseText)
