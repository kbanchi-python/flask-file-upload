import logging
from playhouse.db_url import connect
from peewee import Model
from peewee import IntegerField
from peewee import CharField
from peewee import BlobField

logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = connect("sqlite:///peewee_db.sqlite")

if not db.connect():
    print("接続できませんでした")
    exit()


class File(Model):

    id = IntegerField(primary_key=True)
    name = CharField()
    file_path = CharField()

    class Meta:
        database = db
        table_name = "Files"


db.create_tables([File])
