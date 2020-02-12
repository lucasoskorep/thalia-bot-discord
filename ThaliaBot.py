import asyncio
import discord
import platform
import os

from discord.ext.commands import Bot
from discord import channel, message
from dbmanager.dbmanager import dbmanager
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.DEBUG, filename="server.log")
logger = logging.getLogger(__name__)

load_dotenv()
# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Thalia Bot description", command_prefix="", pm_help=True)

# Set up environment variables for the Database
client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')

print(client_key, username, password, discord_db, address)

# set up the sqlalchemy session object to be used in a threaded manor.

db_man = dbmanager(
    username=username,
    password=password,
    db_location=address,
    db_name=discord_db
)

users = db_man.read_users()
servers = db_man.read_servers()
channels = db_man.read_channels()
print(users)
print(servers)
print(channels)
startup = True

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ID:  {client.user.id}) | Connected to \n'
          f'{len(client.guilds)} servers | Connected to {len(set(client.get_all_members()))} users\n'
          f'--------\n'
          f'Current Discord.py Version: {discord.__version__} | Current Python Version: { platform.python_version()}\n'
          f'--------\n'
          f'Use this link to invite {client.user.name}:\n'
          f'https://discordapp.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions=8'
    )

    return await client.change_presence(
        activity=discord.Game(name='Warframe BABBYYYYYY')
    )  # This is buggy, let us know if it doesn't work.


# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):
    acc = 0
    tmp = ''

    for arg in args:
        acc += 1
        tmp += str(acc) + arg + '\n'
    await client.say(":ping_pong: Pong!\n" + tmp)


import sys
async def parse_channel(channel, message_id):
    messages_db_size = 1000
    counter = 0
    messages = []

    print("STARTING CHANNEL", channel, file=sys.stdout)

    #drop the column's messages from the messages tab.
    try:
        async for message in channel.history(limit=None):
            #TODO: Rework this so that the caching is done behind the scenes
            # \- user should be checked for and added here but hte direct DB and cache calls should be obfuscates
            if int(message.author.id) not in users:
                db_man.create_user(
                    discord_id=message.author.id,
                    name=str(message.author)
                )
                users[int(message.author.id)] = str(message.author)
            if int(message.guild.id) not in servers:
                db_man.create_server(
                    discord_id=message.guild.id,
                    name=str(message.guild)
                )
                servers[int(message.guild.id)] = str(message.guild)

            # create channel if missing
            if int(message.channel.id) not in channels:
                db_man.create_channel(
                    discord_id=message.channel.id,
                    name=str(message.channel)
                )
                channels[int(message.channel.id)] = str(message.channel)

            if message.id != message_id:
                messages.append(
                    {
                        'content':message.content,
                        'timestamp': message.created_at.timestamp(),
                        'author_id':message.author.id,
                        'server_id':message.guild.id,
                        'channel_id':message.channel.id,
                        'message_id':message.id
                    }
                )
            if counter > messages_db_size:
                # for m in messages:
                #     print(f"MESSAGE_ID TO IMPORT IS - {m}")
                db_man.create_messages(messages)
                del messages
                messages = []
                counter = 0
            counter+=1
        if messages:
            db_man.create_messages(messages)
            del messages

        #update the column to being finished.
    except Exception as e:
        print("ERROR THROWN IN THE MESSAGE PARSING")
        logger.exception(e)

    print("ENDED CHANNEL", channel)



def process_message(message):
    print(message.author.id, users)
    # for id, name in users.items():
    #     print(
    #         type(id),
    #         type(author.id)
    #     )
    #     if author.id == id:
    #         print("FOUND THE USER ID")
    #
    # print(server.id, servers)
    # for id, name in servers.items():
    #     print(
    #         type(id),
    #         type(server.id)
    #     )
    #     if server.id == id:
    #         print("FOUND THE SERVER ID")
    #
    # print(channel.id, channels)
    # for id, name in channels.items():
    #     print(
    #         type(id),
    #         type(channel.id)
    #     )
    #     if channel.id == id:
    #         print("FOUND THE CHANNEL ID")
    # print(message.reactions)
    # create user if missing
    if int(message.author.id) not in users:
        db_man.create_user(
            discord_id=message.author.id,
            name=str(message.author)
        )
        users[int(message.author.id)] = str(message.author)
    # create server if missing
    if int(message.guild.id) not in servers:
        db_man.create_server(
            discord_id=message.guild.id,
            name=str(message.guild)
        )
        servers[int(message.guild.id)] = str(message.guild)

    # create channel if missing
    if int(message.channel.id) not in channels:
        db_man.create_channel(
            discord_id=message.channel.id,
            name=str(message.channel)
        )
        channels[int(message.channel.id)] = str(message.channel)
        print("STARTING CHANNEL SEARCH")
    global startup
    if startup == True:
        startup = False
        text_channel_list = []
        for server in client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text':
                    text_channel_list.append(channel)
                print(channel.type)
        print("Starting channel syncing")
        print(text_channel_list)
        for channel in set(text_channel_list):
            #TODO: Only go through channels which are known good
            print(f"Starting channel {channel.name}")
            asyncio.run_coroutine_threadsafe(parse_channel(channel, message.id), client.loop)


    db_man.create_message(
        content=message.content,
        message_id=message.id,
        timestamp=message.created_at.utcnow().timestamp(),
        author_id=message.author.id,
        server_id=message.guild.id,
        channel_id=message.channel.id
    )


@client.event
async def on_message(message):
    print(f"MESSAGE RECIEVED - {message}")
    if message.author.id == client.user.id or message.author.bot:
        return
    print('\n\n\n')
    # Grab message content
    # message_content = message.content
    process_message(message)

    print("Successfully added to the database.")

    if "bot" in message.content.lower():
        await client.send_message(message.channel, "HEY STOP TALKING ABOUT ME")

    print(message.author.id)
    print(message.author == client.user)



print(users)
# Run the discord bot
client.run(client_key)


