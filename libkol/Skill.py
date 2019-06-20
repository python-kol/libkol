class Skill:
    id: int
    buff: bool

    def __init__(self, id: int, buff: bool = False):
        self.id = id
        self.buff = buff

    def __getitem__(self, key: int) -> "Skill":
        return Skill(id=key)
