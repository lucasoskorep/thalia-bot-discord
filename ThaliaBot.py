import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Thalia Bot description", command_prefix="!", pm_help=False)


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
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('Github Link: https://github.com/Habchy/BasicBot')
    print('--------')
    print(
        'You are running BasicBot v2.1')  # Do not change this. This will really help us support you, if you need support.
    print('Created by Habchy#1665')
    return await client.change_presence(
        game=discord.Game(name='PLAYING STATUS HERE'))  # This is buggy, let us know if it doesn't work.


# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):
    await client.say(":ping_pong: Pong!")
    # await asyncio.sleep(3)
    # await client.say(
    #     ":")


# After you have modified the code, feel free to delete the line above so it does not keep popping up everytime you initiate the ping commmand.

client.run('NDExNzQyNDcxMTQwMjc4Mjc2.DWFfGw.CklmyofXxJkk8XRwExVtZwTpocg')