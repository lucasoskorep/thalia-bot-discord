import asyncio
from discord.channel import ChannelType
from dbmanager.tables import *
from uuid import uuid4

class Thalia(object):
    def __init__(self, db_man, bot, oc = None, logger=None):
        self.db_man = db_man
        self.bot = bot
        self.logger = logger
        self.oc = oc

    def process_all_servers(self):
        text_channel_list = []
        for channel in self.bot.get_all_channels():
            if channel.type == ChannelType.text and self.bot.user.id in [member.id for member in channel.members]:
                text_channel_list.append(channel)
        for channel in set(text_channel_list):
            asyncio.run_coroutine_threadsafe(self.parse_channel(channel), self.bot.loop)

    async def parse_channel(self, channel):
        print(f"STARTED PARSING CHANNEL {channel.name}")
        try:
            messages = []
            async for message in channel.history(limit=None):
                self.db_man.validate_message(message)
                messages.append(Thalia.get_message_entity(message))
            if messages:
                self.db_man.create_messages(messages, channel)
            print(f"FINISHED PARSING CHANNEL - {channel}")
        except Exception as e:
            print(e)
            self.logger.exception(e)

    def process_new_message(self, message):
        self.db_man.validate_message(message)
        self.db_man.create_message(Thalia.get_message_entity(message))

    def get_guild_stats(self, message):
        self.db_man.get_channel_stats(message.channel.id)

    def get_file_link(self, file):
        try:
            self.oc.mkdir('thalia_training_data')
        except Exception as e:
            print(e)
        try:
            remote_name = uuid4()
            self.oc.put_file(f'thalia_training_data/{remote_name}.txt', file)
            link_info = self.oc.share_file_with_link(f'thalia_training_data/{remote_name}.txt')
            print("Here is your link: " + link_info.get_link())
            return link_info.get_link()
        except Exception as e:
            print(e)
            return None

    def get_training_data(self, user):
        print(f"getting training data for - {user.name, user.id}")




    @staticmethod
    def get_message_entity(message):
        return Message(
            content=message.content,
            message_id=message.id,
            timestamp=message.created_at.timestamp(),
            author_id=message.author.id,
            server_id=message.guild.id,
            channel_id=message.channel.id
        )
