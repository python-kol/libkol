from .GenericRequest import GenericRequest


class AddMeatToClanStashRequest(GenericRequest):
    "Adds meat to the player's clan stash."

    def __init__(self, session, meat):
        super(AddMeatToClanStashRequest, self).__init__(session)
        self.url = session.server_url + "clan_stash.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "contribute"
        self.requestData["howmuch"] = meat
