import discord
import logging
import platform
import os

from dbmanager.dbmanager import dbmanager
from discord.ext.commands import Bot
from dotenv import load_dotenv
from thalia import Thalia

load_dotenv()

logging.basicConfig(level=logging.DEBUG, filename="server.log")
logger = logging.getLogger(__name__)

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
bot = Bot(description="Thalia Bot description", command_prefix="!", pm_help=True)

# Set up environment variables for the Database
client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')

db_man = dbmanager(
    username=username,
    password=password,
    db_location=address,
    db_name=discord_db
)

thalia = Thalia(db_man, bot, logger)
@bot.event
async def on_ready():
    """
    called when the bot launches and successfully connects to discord
    :return:
    """
    print(f'Logged in as {bot.user.name} ID:  {bot.user.id}) | Connected to \n'
          f'{len(bot.guilds)} servers | Connected to {len(set(bot.get_all_members()))} users\n'
          f'--------\n'
          f'Current Discord.py Version: {discord.__version__} | Current Python Version: { platform.python_version()}\n'
          f'--------\n'
          f'Use this link to invite {bot.user.name}:\n'
          f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8'
    )
    # thalia.process_all_servers()
    return await bot.change_presence(
        activity=discord.Game(name='Warframe BABBYYYYYY')
    )

@bot.command()
async def ping(context):
    """
    Simple ping command from discord.
    :param context: context of the discord message.
    :return: None
    """
    await context.send(":ping_pong: Pong!\n")

@bot.event
async def on_message(message):
    """
    Called whenever a message is recieved in any channel including the bots.
    :param message:
    :return:
    """
    print(f"MESSAGE RECIEVED - {message}")
    await bot.process_commands(message)

    if message.author.id == bot.user.id or message.author.bot:
        return
    print('\n\n\n')

    thalia.process_new_message(message)

    if "bot" in message.content.lower():
        await message.channel.send(message.channel, "HEY STOP TALKING ABOUT ME")

    print(message.author.id)
    print(message.author == bot.user)


bot.run(client_key)
