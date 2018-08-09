from peewee import CharField

from .db import BaseModel


class File(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    hash = CharField()
