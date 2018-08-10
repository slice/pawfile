__all__ = ['db', 'Model']

from peewee import Model
from playhouse.pool import PooledSqliteDatabase

db = PooledSqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db
