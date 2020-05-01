import discord
import logging
import platform
import os

from dbmanager.dbmanager import dbmanager
from discord.ext.commands import Bot
from discord import File
from dotenv import load_dotenv
from uuid import uuid4
from owncloud import Client, ShareInfo
from thalia import Thalia

load_dotenv()
# logging.basicConfig(level=logging.DEBUG, filename="server.log")
# logger = logging.getLogger(__name__)

bot = Bot(description="Thalia Bot description", command_prefix="!", pm_help=True)

# Set up environment variables for the Database
client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')
oc_username = os.getenv("NEXTCLOUD_USERNAME", "username")
oc_password = os.getenv("NEXTCLOUD_PASSWORD", "pw")
db_man = dbmanager(
    username=username,
    password=password,
    db_location=address,
    db_name=discord_db
)

oc = Client('https://nextcloud.chaoticdevelopment.com/')
oc.login(oc_username, oc_password)

thalia = Thalia(db_man, bot, oc)

@bot.event
async def on_ready():
    """
    called when the bot launches and successfully connects to discord
    :return:
    """
    print(f'Logged in as {bot.user.name} ID:  {bot.user.id}) | Connected to \n'
          f'{len(bot.guilds)} servers | Connected to {len(set(bot.get_all_members()))} users\n'
          f'--------\n'
          f'Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}\n'
          f'--------\n'
          f'Use this link to invite {bot.user.name}:\n'
          f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8'
          )
    return await bot.change_presence(
        activity=discord.Game(name='Warframe BABBYYYYYY')
    )


@bot.command()
async def get_training_data(context):
    print(context.message.author.id)
    df = thalia.get_training_data(context.message.author)
    filename = f"{uuid4()}.csv"
    remote_filename = f"thalia_training_data/{filename}"
    df.to_csv(filename, index=False, quoting=2)
    print("Throwing file to own cloud")
    oc.put_file(remote_filename, filename)
    print("Getting file link from own cloud")
    link = oc.share_file_with_link(remote_filename)
    await context.send(f"Here is your file: {link.get_link()}")
    # change the remote directory to a docker variable if possible.
    # Delete local file


@bot.command()
async def ping(context):
    """
    Simple ping command from discord.
    :param context: context of the discord message.
    :return: None
    """
    await context.send(":ping_pong: Pong!\n")


@bot.command()
async def repopulate(context):
    """
    Simple ping command from discord.
    :param context: context of the discord message.
    :return: None
    """
    thalia.process_all_servers()

    await context.send("REPOPULATING SERVER HISTORY - THIS MAY TAKE A SECOND!")


@bot.event
async def on_message(message):
    """
    Called whenever a message is recieved in any channel including the bots.
    :param message:
    :return:
    """
    print(f"{message}")
    if message.author.id == bot.user.id or message.author.bot:
        return
    await bot.process_commands(message)
    thalia.process_new_message(message)
    # thalia.get_guild_stats(message)
    # thalia.get_training_data(message.author)


bot.run(client_key)
