from pykollib.database import ItemDatabase  # @UnusedImport
from pykollib.request.GenericRequest import GenericRequest

# TODO: This request needs to be redone, since the BHH interface has changed
class BountyHunterRequest(GenericRequest):
    """Interacts with the Bounty Hunter Hunter in the Forest Village."""

    VISIT = None
    BUY = "buy"

    def __init__(self, session, action=None, item=None, quantity=None):
        """Initialize a Bounty Hunter Hunter request.
        
        Args:
            session: A valid logged in session.
            action: Optional action. If None, the request just "visits" the Bounty 
                Hunter Hunter and determines which bounties are available.
                Possible values:
                    'buy': Buy an item with your filthy lucre
                    'giveup_low': Abandon the easy bounty assignment
                    'giveup_high': Abandon the hard bounty assignment
                    'giveup_special': Abandon the special bounty assignment
                    'takelow': Accept the easy bounty assignment
                    'takehigh': Accept the hard bounty assignment
                    'takespecial': Accept the special bounty assignment
            item: Optional id of the item (e.g. 2463 for Manual of Transcendent 
                Olfaction) being bought from the Bounty Hunter Hunter with your
                filthy lucre.
            quantity: Optional number of items being purchased for filthy lucre.
        """
        super(BountyHunterRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "bounty.php"

        self.requestData["pwd"] = session.pwd

        if action:
            self.requestData["action"] = action
        if quantity:
            self.requestData["howmany"] = quantity
        if item:
            self.requestData["whichitem"] = item

    def parseResponse(self):
        """
        Returns a dict with the following possible elements:
            easyBountyAvailable: boolean
            hardBountyAvailable: boolean
            specialBountyAvailable: boolean
            easyBountyActive: boolean
            hardBountyActive: boolean
            specialBountyActive: boolean
        """
        response = {}

        easyBountyAvailable = self.searchNamedPattern("easyBountyAvailable")
        hardBountyAvailable = self.searchNamedPattern("hardBountyAvailable")
        specialBountyAvailable = self.searchNamedPattern("specialBountyAvailable")
        easyBountyActive = self.searchNamedPattern("easyBountyActive")
        hardBountyActive = self.searchNamedPattern("hardBountyActive")
        specialBountyActive = self.searchNamedPattern("specialBountyActive")

        response["easyBountyAvailable"] = easyBountyAvailable is not None
        response["hardBountyAvailable"] = hardBountyAvailable is not None
        response["specialBountyAvailable"] = specialBountyAvailable is not None
        response["easyBountyActive"] = easyBountyActive is not None
        response["hardBountyActive"] = hardBountyActive is not None
        response["specialBountyActive"] = specialBountyActive is not None
        self.responseData = response
