import asyncio
import sys
from dbmanager.tables import *


class Thalia(object):
    def __init__(self, db_man, bot, logger=None):
        self.db_man = db_man
        self.bot = bot
        self.logger = logger
        self.db_size_limit = 1000

    def process_all_servers(self):
        text_channel_list = []
        for server in self.bot.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text':
                    text_channel_list.append(channel)
                print(channel.type)
        print("Starting channel syncing")
        print(text_channel_list)
        for channel in set(text_channel_list):
            # TODO: Only go through channels which are known good
            print(f"Starting channel {channel.name}")
            asyncio.run_coroutine_threadsafe(self.parse_channel(channel), self.bot.loop)

    async def parse_channel(self, channel):
        messages_db_size = 1000
        counter = 0
        messages = []
        print(f"Parsing channel {channel.name}")
        # drop the column's messages from the messages tab.
        try:
            async for message in channel.history(limit=None):
                self.validate_message(message)
                messages.append(
                    get_message_entity(message)
                )
                if counter > messages_db_size:
                    self.db_man.create_messages(messages)
                    del messages
                    messages = []
                    counter = 0
                counter += 1
            if messages:
                self.db_man.create_messages(messages)
                del messages
        except Exception as e:
            print("ERROR THROWN IN THE MESSAGE PARSING")
            self.logger.exception(e)

        print("ENDED CHANNEL", channel)

    def validate_message(self, message):
        self.db_man.validate_user(message.author)
        self.db_man.validate_guild(message.guild)
        self.db_man.validate_channel(message.channel)

    def process_new_message(self, message):
        print(f"processing new message - {message}")
        self.validate_message(message)
        self.db_man.create_message(get_message_entity(message))
        print("finished saving message to DB")


def get_message_entity(message):
    return Message(
        content=message.content,
        message_id=message.id,
        timestamp=message.created_at.utcnow().timestamp(),
        author_id=message.author.id,
        server_id=message.guild.id,
        channel_id=message.channel.id
    )
