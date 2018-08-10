__all__ = ['db', 'Model']

from peewee import Model, SqliteDatabase

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db
