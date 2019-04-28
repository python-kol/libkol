import TestData
from pykollib.request.BountyHunterRequest import BountyHunterRequest
import unittest

class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        
        # Don't do test if easy bounty is not available
        bountyRequest = BountyHunterRequest(s)
        response = bountyRequest.doRequest()
        self.assertTrue(response['easyBountyAvailable'], 
                        "easyBounty should be available for this test")
        self.assertFalse(response['easyBountyActive'], 
                         "easyBounty should not be active for this test")

        # Accept the easy bounty
        acceptEasyReq = BountyHunterRequest(s, action='takelow')
        response = acceptEasyReq.doRequest()
        self.assertTrue(response['easyBountyActive'], 
                        "easyBounty should be active after an accept")
        self.assertFalse(response['easyBountyAvailable'], 
                         "easyBounty should not be available after an accept")
        
        # Abandon the easy bounty (so this test can only be done once a day :-)
        abandonEasyReq = BountyHunterRequest(s, action='giveup_low')
        response = abandonEasyReq.doRequest()
        self.assertFalse(response['easyBountyAvailable'], 
                        "easyBounty should be not be available after giving up"
                        + " (only one offer per day)")
        self.assertFalse(response['easyBountyActive'], 
                         "easyBounty should not be active after giving up")
            
