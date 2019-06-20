from datetime import tzinfo, timedelta, datetime

phase_names = {
    0: "new moon",
    1: "waxing crescent",
    2: "first quarter",
    3: "waxing gibbous",
    4: "full moon",
    5: "waning gibbous",
    6: "third quarter",
    7: "waning crescent",
}

class KLT(tzinfo):
    """
    Kingdom of Loathing Time
    """

    def utcoffset(self, dt):
        return timedelta(hours=-3, minutes=-30)

    def tzname(self, dt):
        return "KLT"

    def dst(self, dt):
        return timedelta(0)

class koldate:
    EPOCH = datetime(2005, 9, 18, 0, 0, 0, tzinfo=KLT())
    WHITE_WEDNESDAY = datetime(2005, 10, 28, 0, 0, 0, tzinfo=KLT());

    MONTHS = [
        "Jarlsuary",
        "Frankuary",
        "Starch",
        "April",
        "Martinus",
        "Bill",
        "Bor",
        "Petember",
        "Carlvember",
        "Porktober",
        "Boozember",
        "Dougtember",
    ]

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __lt__(self, value):
        return self.days < value.days

    def __lte__(self, value):
        return self.days <= value.days

    def __gt__(self, value):
        return self.days > value.days

    def __gte__(self, value):
        return self.days > value.days

    def __eq__(self, value):
        return self.days == value.days

    def __sub__(self, value):
        return self.days - value.days

    @property
    def COLLISION(self):
        return koldate(2, 8, 2)

    @classmethod
    def today(cls):
        return cls.from_gregorian(datetime.today())

    @classmethod
    def get_phase_name(cls, phase: int):
        return phase_names.get(phase, "unknown")

    @classmethod
    def from_gregorian(cls, date: datetime):
        delta = date.replace(tzinfo=KLT()) - cls.EPOCH
        days = delta.days

        year, year_day = divmod(days, 96)
        month, day = divmod(year_day, 8)

        return cls(year, month, day)

    @staticmethod
    def get_hamburglar_light(ronald_phase: int, grimace_phase: int, hamburglar_phase: int) -> int:
        if hamburglar_phase == 0:
            return -1 if 0 < grimace_phase < 5 else 1

        if hamburglar_phase == 1:
            return -1 if 3 < grimace_phase < 8 else 1

        if hamburglar_phase == 2:
        	return 1 if 3 < grimace_phase < 8 else 0

        if hamburglar_phase == 4:
        	return 1 if 0 < grimace_phase < 5 else 0

        if hamburglar_phase == 5:
        	return 1 if 3 < ronald_phase < 8 else 0

        if hamburglar_phase == 7:
        	return 1 if 0 < ronald_phase < 5 else 0

        if hamburglar_phase == 8:
        	return -1 if 0 < ronald_phase < 5 else 1

        if hamburglar_phase == 9:
        	return -1 if 3 < ronald_phase < 8 else 1

        if hamburglar_phase == 10:
            return (
                self.get_hamburglar_light(ronald_phase, grimace_phase, 4) +
                self.get_hamburglar_light(ronald_phase, grimace_phase, 5)
            )

        return 0

    def strftime(self, format: str) -> str:
        tokens = {
            "d": f"{self.day:02}",
            "b": self.month_name[0:3],
            "B": self.month_name,
            "m": f"{self.month:02}",
            "y": f"{self.year:02}",
            "Y": self.year
        }
        for token, replacement in tokens:
            format = format.replace(f"%{token}", replacement)
        return format

    @property
    def days(self):
        return (self.year * 96) + (self.month * 8) + self.day

    @property
    def month_name(self) -> str:
        return self.MONTHS[self.month]

    @property
    def ronald_phase(self) -> int:
        return self.day

    @property
    def grimace_phase(self) -> int:
        return ((self.month % 2) * 4) + self.day // 2

    @property
    def hamburglar_phase(self) -> int:
        if self < self.COLLISION:
            return -1

        return ((self - self.COLLISION) * 2) % 11

    @property
    def ronald_light(self) -> int:
        if self.ronald_phase < 5:
            return self.ronald_phase

        return 8 - self.ronald_phase

    @property
    def grimace_light(self) -> int:
        if self.grimace_phase < 5:
            return self.grimace_phase

        return 8 - self.grimace_phase

    @property
    def grimace_darkness(self) -> int:
        return 4 - self.grimace_light + self.hamburglar_darkness;

    @property
    def hamburglar_light(self) -> int:
        return self.get_hamburglar_light(self.ronald_phase, self.grimace_phase, self.hamburglar_phase)

    @property
    def hamburglar_darkness(self):
        if self.hamburglar_phase < 8:
            return self.get_hamburglar_light((self.ronald_phase + 8) % 8, (self.grimace_phase + 8) % 8, self.hamburglar_phase)

        return 0 if self.hamburglar_light > 0 else 0

    @property
    def moonlight(self) -> int:
        return self.ronald_light + self.grimace_light + self.hamburglar_light
