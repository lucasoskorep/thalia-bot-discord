from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from dbmanager.tables import User, Server, Channel, Message, _base
import threading

lock = threading.Lock()

class session_manager_wrapper(object):
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session()

    def __exit__(self,type, value, traceback):
        self.session.remove()

class dbmanager(object):

    def __init__(self, username, password, db_location, db_name, max_transaction_size = 1000):

        engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + db_location + '/' + db_name)
        _base.metadata.create_all(engine)
        self.session_factory = sessionmaker(bind=engine)
        self.create_session = session_manager_wrapper(
            scoped_session(self.session_factory)
        )
        self.users = self.get_user_cache()
        self.servers = self.get_server_cache()
        self.channels = self.get_channel_cache()
        self.max_transaction_size = max_transaction_size

    def create_message(self, message):
        with self.create_session as sess:
            sess.add(message)
            sess.commit()

    def create_messages(self, messages, channel):
        with lock, self.create_session as sess:
            for message in messages:
                sess.merge(message)
            print(f"COMMITTING CHANNEL - {channel.name}"
                  f"Messages added - {len(messages)}")
            sess.commit()

    def read_messages(self):
        with self.create_session as sess:
            messages = []
            for message in sess.query(Message):
                messages.append(message)
            return messages

    def create_user(self, discord_id, name):
        with self.create_session as sess:
            new_user = User(
                discord_id=discord_id,
                name=name
            )
            sess.add(new_user)
            sess.commit()

    def create_server(self, discord_id, name):
        with self.create_session as sess:

            new_server = Server(
                discord_id=discord_id,
                name=name
            )
            sess.add(new_server)
            sess.commit()


    def create_channel(self, discord_id, name, server_id):
        with self.create_session as sess:
            new_channel = Channel(
                server_id=server_id,
                discord_id=discord_id,
                name=name
            )
            sess.add(new_channel)
            sess.commit()


    def get_server_cache(self):
        with self.create_session as sess:
            servers = {}
            for id, name in sess.query(Server.discord_id, Server.name):
                servers[id] = name
        return servers

    def get_channel_cache(self):
        with self.create_session as sess:

            channels = {}
            for id, name in sess.query(Channel.discord_id, Channel.name):
                channels[id] = name
        return channels

    def get_user_cache(self):
        with self.create_session as sess:
            users = {}
            for id, name in sess.query(User.discord_id, User.name):
                users[id] = name
        return users

    def create_test_setup(self):
        with self.create_session as sess:

            new_person = User(discord_id=69, name="user")
            sess.add(new_person)
            sess.commit()

            new_server = Server(discord_id=6969, name="server")
            sess.add(new_server)
            sess.commit()

            new_channel = Channel(server_id=6969, discord_id=696969, name="channel")
            sess.add(new_channel)
            sess.commit()

            new_message = Message(
                content="test content",
                message_id=12312312,
                author_id=69,
                server_id=6969,
                channel_id=696969,
                timestamp=1.0
            )
            sess.add(new_message)
            sess.commit()


    def validate_message(self, message):
        self.validate_guild(message.guild)
        self.validate_channel(message.channel, message.guild)
        self.validate_user(message.author)

    def validate_user(self, author):
        if int(author.id) not in self.users:
            self.create_user(
                discord_id=author.id,
                name=str(author)
            )
            self.users[int(author.id)] = str(author)

    def validate_guild(self, guild):
        if int(guild.id) not in self.servers:
            self.create_server(
                discord_id=guild.id,
                name=str(guild)
            )
            self.servers[int(guild.id)] = str(guild)

    def validate_channel(self, channel, guild):
        if int(channel.id) not in self.channels:
            self.create_channel(
                discord_id=channel.id,
                name=str(channel),
                server_id=guild.id
            )
            self.channels[int(channel.id)] = str(channel)
            print("STARTING CHANNEL SEARCH")

    def get_training_dataset(self, userID):
        with self.create_session as sess:
            for message in sess.query(Message).filter().order_by().limit(3):

    def get_channel_stats(self, channelID):

        with self.create_session as sess:
            print("attempting to print all messages")
            print(channelID)
            # Get the channel specific stats - pull basics from server, and channel tables, and then print last 3 messages from channel.
            for message in sess.query(Message).filter(Message.channel_id == channelID).order_by(desc(Message.timestamp)).limit(3):
                print(message)

            #     Channel stats

            # self.Session.remove()