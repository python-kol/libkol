import libkol

from .request import Request


class choice(Request):
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param choice: The id of the choice
    :param option: The number option to submit
    """

    def __init__(self, session: "libkol.Session", choice: int, option: int) -> None:
        super().__init__(session)
        params = {"whichchoce": choice, "option": option}
        self.request = session.request("choice.php", params=params, pwd=True)
