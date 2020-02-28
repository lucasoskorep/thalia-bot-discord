from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text, BIGINT, FLOAT, DECIMAL

_base = declarative_base()


class User(_base):
    __tablename__ = 'user'
    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __repr__(self):
        return f"<User(name='{self.name}', discord_id='{self.discord_id}')>"


class Channel(_base):
    __tablename__ = 'channel'

    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)
    server_id = Column(BIGINT, ForeignKey('server.discord_id'),  nullable=False, index=True)

    def __repr__(self):
        return f"<Channel(name='{self.name}', discord_id='{self.discord_id}')>"


class Server(_base):
    __tablename__ = 'server'

    discord_id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __repr__(self):
        return f"<Server(name='{self.name}', discord_id='{self.discord_id}')>"


class Message(_base):
    __tablename__ = 'messages'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.

    content = Column(Text, nullable=False)
    timestamp = Column(DECIMAL, nullable=False)
    message_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    author_id = Column(BIGINT, ForeignKey('user.discord_id'), nullable=False, index=True)
    server_id = Column(BIGINT, ForeignKey('server.discord_id'), nullable=False, index=True)
    channel_id = Column(BIGINT, ForeignKey('channel.discord_id'), nullable=False, index=True, primary_key=True)
    server = relationship('Server', foreign_keys=[server_id])
    author = relationship('User', foreign_keys=[author_id])
    channel = relationship('Channel', foreign_keys=[channel_id])

    def __repr__(self):
        return "<Message(content='%s', messsage_id='%s', author_id='%s', server_id='%s', channel_id='%s')>" % (
            self.content, self.message_id, self.author_id, self.server_id, self.channel_id)
