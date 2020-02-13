from sqlalchemy import create_engine
from dbmanager import dbmanager
from dbmanager.tables import _base
import os

from dotenv import load_dotenv

load_dotenv()

client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')
engine = create_engine('mysql+pymysql://' + username +':' + password +'@'+address+'/'+discord_db)

_base.metadata.create_all(engine)
db_man = dbmanager(
    username=username,
    password=password,
    db_location=address,
    db_name=discord_db
)

db_man.create_test_setup()


