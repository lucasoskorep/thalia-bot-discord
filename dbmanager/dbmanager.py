from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from dbmanager.db_classes import User, Server, Channel, Message
import threading

lock = threading.Lock()

class dbmanager(object):
    """

    """

    def __init__(self, username, password, db_location, db_name):
        """

        :param username:
        :param password:
        :param db_location:
        :param db_name:
        """
        engine = create_engine('mysql+pymysql://' + username +':' + password +'@'+db_location+'/'+db_name)
        self.session_factory = sessionmaker(bind=engine)
        global Session
        Session = scoped_session(self.session_factory)

    def create_test_setup(self):
        """

        :return:
        """
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
            message_id = 12312312,
            author_id = 69,
            server_id = 6969,
            channel_id = 696969
        )
        sess.add(new_message)
        sess.commit()

        Session.remove()

    def create_message(self, content, timestamp, message_id, author_id, server_id, channel_id):
        """

        :param content:
        :param message_id:
        :param author_id:
        :param server_id:
        :param channel_id:
        :return:
        """
        global Session
        sess = Session()

        new_message = Message(
            content = content,
            timestamp = timestamp,
            message_id = message_id,
            author_id = author_id,
            server_id = server_id,
            channel_id = channel_id
        )
        sess.add(new_message)
        sess.commit()

        Session.remove()

    def create_messages(self, messages):
        with lock:
            global Session
            sess = Session()
            for message in messages:
                new_message = Message(
                    content = message['content'],
                    timestamp= message['timestamp'],
                    message_id = message['message_id'],
                    author_id = message['author_id'],
                    server_id = message['server_id'],
                    channel_id = message['channel_id']
                )
                sess.add(new_message)
            print(
                f"COMMITTING CHANNEL - {messages[0]['channel_id']}")
            # print(messages)
            print(len(messages))

            # try:
            sess.commit()
            # except Exception as e:
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
        """

        :param content:
        :param message_id:
        :param author_id:
        :param server_id:
        :param channel_id:
        :return:
        """
        global Session
        sess = Session()

        new_user = User(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_user)
        sess.commit()

        Session.remove()

    def read_users(self):
        """

        :return:
        """
        global Session
        sess = Session()
        users = {}
        for id, name in sess.query(User.discord_id, User.name):
            users[id] = name
        Session.remove()
        return users


    def create_server(self, discord_id, name):
        """

        :param content:
        :param message_id:
        :param author_id:
        :param server_id:
        :param channel_id:
        :return:
        """
        global Session
        sess = Session()

        new_server = Server(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_server)
        sess.commit()

        Session.remove()

    def read_servers(self):
        """

        :return:
        """

        global Session
        sess = Session()
        servers = {}
        for id, name in sess.query(Server.discord_id, Server.name):
            servers[id] = name
        Session.remove()
        return servers

    def create_channel(self, discord_id, name):
        """

        :param content:
        :param message_id:
        :param author_id:
        :param server_id:
        :param channel_id:
        :return:
        """
        global Session
        sess = Session()

        new_channel = Channel(
            discord_id=discord_id,
            name=name
        )
        sess.add(new_channel)
        sess.commit()

        Session.remove()

    def read_channels(self):
        """

        :return:
        """
        global Session
        sess = Session()
        channels = {}
        for id, name in sess.query(Channel.discord_id, Channel.name):
            channels[id] = name
        Session.remove()
        return channels
