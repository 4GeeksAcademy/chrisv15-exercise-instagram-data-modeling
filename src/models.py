import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250))
    posts = relationship("Post", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.user_to_id', back_populates="user_to")
    following = relationship("Follower", foreign_keys='Follower.user_from_id', back_populates="user_from")
    stories = relationship("Story", back_populates="user")
    messages_sent = relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    messages_received = relationship("Message", foreign_keys='Message.recipient_id', back_populates="recipient")
    notifications = relationship("Notification", back_populates="user")

class Post(Base):
    __tablename__ = 'post'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'), nullable=False)
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('user.ID'))
    post_id = Column(Integer, ForeignKey('post.ID'))
    author = relationship("User")

class Like(Base):
    __tablename__ = 'like'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    post_id = Column(Integer, ForeignKey('post.ID'))

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.ID'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.ID'), nullable=False)
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

class Media(Base):
    __tablename__ = 'media'
    ID = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type_enum'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.ID'))
    post = relationship("Post", back_populates="media")

class Story(Base):
    __tablename__ = 'story'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    user = relationship("User", back_populates="stories")
    media = relationship("Media", back_populates="story")
    duration = Column(Integer)
    views = relationship("StoryView", back_populates="story")

class StoryView(Base):
    __tablename__ = 'story_view'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    story_id = Column(Integer, ForeignKey('story.ID'))
    story = relationship("Story", back_populates="views")

class Message(Base):
    __tablename__ = 'message'
    ID = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.ID'))
    recipient_id = Column(Integer, ForeignKey('user.ID'))
    content = Column(String(250))
    sent_date = Column(DateTime)
    read = Column(Boolean)
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="messages_received")

class Notification(Base):
    __tablename__ = 'notification'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    content = Column(String(250))
    created_date = Column(DateTime)
    user = relationship("User", back_populates="notifications")

render_er(Base, 'diagram.png')
