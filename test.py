import os
import time
from dbmanager.dbmanager import dbmanager

client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')


print(client_key, username, password, address, discord_db)


db_man = dbmanager(
    username = username,
    password = password,
    db_location = address,
    db_name = discord_db
)
t = time.time()
messages = db_man.read_messages()
print(time.time() - t)
for message in messages:
    print(message)
    print(message.author)
    print(message.server)
    print(message.channel)