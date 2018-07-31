import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform


from pprint import pprint

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Thalia Bot description", command_prefix="", pm_help=False)


# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
        len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')


    return await client.change_presence(
        game=discord.Game(name='Warframe BABBYYYYYY')
    )  # This is buggy, let us know if it doesn't work.


# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):
    acc = 0
    tmp = ''

    for arg in args:
        acc+= 1
        tmp += str(acc) +  arg + '\n'
    await client.say(":ping_pong: Pong!\n" + tmp)
    # await asyncio.sleep(3)
    # await client.say(
    #     ":")



def add_message_to_database(message):
    print(message)


@client.event
async def on_message(message):
    if message.author.id == client.user.id or message.author.bot:
        return
    print('\n\n\n')
    #Grab message content
    # message_content = message.content
    # author = message.author
    # timestamp = message.timestamp
    # channel = message.channel
    # mentions = message.mentions
    # channel_mentions = message.channel_mentions
    # server = message.server
    if "bot" in message.content.lower():
        await client.send_message(message.channel, "HEY STOP TALKING ABOUT ME")

    print(message.author.id)
    print(message.author == client.user)
    # try:
    #     # await client.send_message(message.channel, message.content)
    # except Exception as e:
    #     #Add in tracing and failure warning for myself here.
    #     print(e)

# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.

client.run('NDEyMTkwODE3OTkwNzM3OTQz.DkFYdA.mVu_HAZZX2Ya-CbLqH13uQjNjwE')