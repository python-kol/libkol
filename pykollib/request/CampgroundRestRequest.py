from pykollib.request.GenericRequest import GenericRequest


class CampgroundRestRequest(GenericRequest):
    "Rests at the user's campground."

    def __init__(self, session):
        super(CampgroundRestRequest, self).__init__(session)
        self.url = session.server_url + "campground.php?action=rest"
