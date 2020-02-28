import asyncio
from dbmanager.tables import *


class Thalia(object):
    def __init__(self, db_man, bot, logger=None):
        self.db_man = db_man
        self.bot = bot
        self.logger = logger
        self.db_size_limit = 5000

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
        """
        TODO: Why is this fucker async

        :param channel:
        :return:
        """
        counter = 0
        messages = []
        print(f"Parsing channel {channel.name}")
        # drop the column's messages from the messages tab.
        try:
            async for message in channel.history(limit=None):
                self.db_man.validate_message(message)
                messages.append(
                    get_message_entity(message)
                )
                if counter > self.db_size_limit:
                    self.db_man.create_messages(messages, channel)
                    del messages
                    messages = []
                    counter = 0
                counter += 1
            if messages:
                self.db_man.create_messages(messages, channel)
                del messages
        except Exception as e:
            print("ERROR THROWN IN THE MESSAGE PARSING")
            self.logger.exception(e)
            print(e)

        print("ENDED CHANNEL", channel)


    def process_new_message(self, message):
        print(f"processing new message - {message}")
        self.db_man.validate_message(message)
        self.db_man.create_message(get_message_entity(message))
        print("finished saving message to DB")


def get_message_entity(message):
    return Message(
        content=message.content,
        message_id=message.id,
        timestamp=message.created_at.timestamp(),
        author_id=message.author.id,
        server_id=message.guild.id,
        channel_id=message.channel.id
    )
