import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

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

@client.event
async def on_message(message):

    print('\n\n\n')
    print(message.content)
    print(message.channel)
    print(message.author)
    print(client.user)
    print(message.author == client.user)
    if message.author != client.user:
        await client.send_message(message.channel, message.content)


# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.

client.run('NDEyMTkwODE3OTkwNzM3OTQz.DWGqSQ.1hva_cKDwQcsQvxRwpjJhABqSKo')