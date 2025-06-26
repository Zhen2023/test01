#./models.py
from tkinter import CASCADE
from sqlalchemy import Nullable
import datetime as dt
from my_flask_app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin ,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable = False)# 唯一且不可为空
    name = db.Column(db.String(80),nullable=False) 
    tel = db.Column(db.String(11))
    email = db.Column(db.String(100),unique=True,nullable = False)
    note = db.Column(db.String(200))
    password = db.Column(db.String(256))
    posts = db.relationship('Post',back_populates='author',lazy='dynamic',cascade='all,delete-orphan')
    comments = db.relationship('Comment',back_populates='author',lazy='dynamic',cascade='all,delete-orphan')
    

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def __repr__(self):
        return f"User {self.name}"
    


post_tags = db.Table('post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id'),primary_key = True),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'),primary_key = True)
    )

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(5000),nullable=False)
    # author_name = db.Column(db.String(50),nullable=False)
    summary = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime,default=dt.datetime.now)
    update_time = db.Column(db.DateTime,default=dt.datetime.now,onupdate=dt.datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    tags = db.relationship('Tag',secondary = post_tags,lazy ='select',backref=db.backref('posts',lazy='dynamic'))
    likes = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    author = db.relationship('User',back_populates='posts')
    comments = db.relationship('Comment',back_populates='post',lazy='dynamic',cascade='all,delete-orphan')


    
    def __repr__(self):
        return f"<Post '{self.title}'>"

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique = True,nullable = False)
    

    def __repr__(self):
        return f"<Tags'{self.name}'>"

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,index=True,default=dt.datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    author = db.relationship('User',back_populates='comments')
    post = db.relationship('Post',back_populates='comments')

    def __repr__(self):
        return f"<Comment '{self.content}'>"

