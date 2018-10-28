import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbmanager.dbmanager import dbmanager

client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')

dbman = dbmanager(
    username=username,
    password=password,
    db_location=address,
    db_name=discord_db
)


# dbman.create_test_setup()
# dbman.create_message(
#     content="hello there",
#     message_id=69,
#     author_id=69,
#     server_id=6969,
#     channel_id=696969
# )
