from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from dbmanager.tables import User, Server, Channel, Message
import threading

lock = threading.Lock()
# Move to peewee if possible

class dbmanager(object):

    def __init__(self, username, password, db_location, db_name):
        global Session
        engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + db_location + '/' + db_name)
        self.session_factory = sessionmaker(bind=engine)
        Session = scoped_session(self.session_factory)
        self.users = self.get_user_cache()
        self.servers = self.get_server_cache()
        self.channels = self.get_channel_cache()

    def create_message(self, message):
        global Session
        sess = Session()
        
        sess.add(message)
        sess.commit()
        Session.remove()

    def create_messages(self, messages):
        with lock:
            global Session
            sess = Session()
            for message in messages:
                sess.add(message)
            print(f"COMMITTING CHANNEL - {messages[0]['channel_id']}"
                  f"Messages added - {len(messages)}")
            sess.commit()
            Session.remove()

    def read_messages(self):
        global Session
        sess = Session()
        messages = []
        for message in sess.query(Message):
            messages.append(message)
        Session.remove()
        return messages

    def create_user(self, discord_id, name):
        global Session
        sess = Session()

        new_user = User(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_user)
        sess.commit()

        Session.remove()

    def create_server(self, discord_id, name):
        global Session
        sess = Session()

        new_server = Server(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_server)
        sess.commit()

        Session.remove()

    def create_channel(self, discord_id, name):
        global Session
        sess = Session()

        new_channel = Channel(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_channel)
        sess.commit()

        Session.remove()

    def get_server_cache(self):
        global Session
        sess = Session()
        servers = {}
        for id, name in sess.query(Server.discord_id, Server.name):
            servers[id] = name
        Session.remove()
        return servers

    def get_channel_cache(self):
        global Session
        sess = Session()
        channels = {}
        for id, name in sess.query(Channel.discord_id, Channel.name):
            channels[id] = name
        Session.remove()
        return channels

    def get_user_cache(self):
        global Session
        sess = Session()
        users = {}
        for id, name in sess.query(User.discord_id, User.name):
            users[id] = name
        Session.remove()
        return users

    def create_test_setup(self):
        global Session
        sess = Session()

        new_person = User(discord_id=69, name="user")
        sess.add(new_person)
        sess.commit()

        new_server = Server(discord_id=6969, name="server")
        sess.add(new_server)
        sess.commit()

        new_channel = Channel(discord_id=696969, name="channel")
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

        Session.remove()

    def validate_message(self, message):
        self.validate_user(message.user)
        self.validate_guild(message.guild)
        self.validate_channel(message.channel)

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

    def validate_channel(self, channel):
        if int(channel.id) not in self.channels:
            self.create_channel(
                discord_id=channel.id,
                name=str(channel)
            )
            self.channels[int(channel.id)] = str(channel)
            print("STARTING CHANNEL SEARCH")