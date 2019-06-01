from peewee import Model, SqliteDatabase


class KolContainer:
    def __init__(self, session=None):
        self.session = session

    def init(self, session):
        self.session = session


db = SqliteDatabase(None)
db_kol = KolContainer(None)


class BaseModel(Model):
    class Meta:
        database = db
        kol_session = db_kol

        @property
        def kol(self):
            return self.kol_session.session
