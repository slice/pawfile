__all__ = ['db', 'Model']

from peewee import Model, SqliteDatabase

db = SqliteDatabase('files.db')


class BaseModel(Model):
    class Meta:
        database = db
