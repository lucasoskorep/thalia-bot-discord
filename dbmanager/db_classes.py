import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.types import Text, String, BIGINT, DECIMAL, TIMESTAMP, FLOAT

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __repr__(self):
        return "<User(name='%s', dicord_id='%s')>" % (
            self.name, self.discord_id)

class Channel(Base):
    __tablename__ = 'channel'

    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __repr__(self):
        return "<User(name='%s', dicord_id='%s')>" % (
            self.name, self.discord_id)

class Server(Base):
    __tablename__ = 'server'

    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __repr__(self):
        return "<User(name='%s', dicord_id='%s')>" % (
            self.name, self.discord_id)


class ServerChannel(Base):
    __tablename__ = 'server_channel'

    id = Column(Integer, primary_key=True)

    server_id = Column(BIGINT, ForeignKey('server.discord_id'), nullable=False)
    channel_id = Column(BIGINT, ForeignKey('channel.discord_id'), nullable=False)


class UserServer(Base):
    __tablename__ = 'user_server'

    id = Column(Integer, primary_key=True)

    author_id = Column(BIGINT, ForeignKey('user.discord_id'), nullable=False)
    server_id = Column(BIGINT, ForeignKey('server.discord_id'), nullable=False)
    server = relationship('Server', foreign_keys=[server_id])
    author = relationship('User', foreign_keys=[author_id])


class UserToNames(Base):
    __tablename__ = 'user_to_name'

    id = Column(Integer, primary_key=True)
    user = Column(BIGINT, ForeignKey('user.discord_id'), nullable=False)
    name = Column(String(250), nullable=False)


class Message(Base):
    __tablename__ = 'messages'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.

    content = Column(Text, nullable=False)
    timestamp = Column(DECIMAL , nullable=False)
    message_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    author_id = Column(BIGINT, ForeignKey('user.discord_id'), nullable=False, index=True)
    server_id = Column(BIGINT, ForeignKey('server.discord_id'), nullable=False, index = True)
    channel_id = Column(BIGINT, ForeignKey('channel.discord_id'), nullable=False, index=True, primary_key=True)
    server = relationship('Server', foreign_keys=[server_id])
    author = relationship('User', foreign_keys=[author_id])
    channel = relationship('Channel', foreign_keys=[channel_id])

    def __repr__(self):
        return "<Message(content='%s', messsage_id='%s', author_id='%s', server_id='%s', channel_id='%s')>" % (
            self.content, self.message_id, self.author_id, self.server_id, self.channel_id)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.

# Grab the password from the environment
# Grab the username from the environment
# Grab the address from the environment

from dotenv import load_dotenv

load_dotenv()
client_key = os.getenv('DISCORD_CLIENT_KEY', '0')
username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
address = os.getenv('MYSQL_ADDRESS', 'localhost:3306')
discord_db = os.getenv('MYSQL_DISCORD_DB', 'THALIA')
engine = create_engine('mysql+pymysql://' + username +':' + password +'@'+address+'/'+discord_db)
#
# # Create all tables in the engine. This is equivalent to "Create Table"
# # statements in raw SQL.
Base.metadata.create_all(engine)
