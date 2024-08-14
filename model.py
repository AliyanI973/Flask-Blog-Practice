import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from flask_login import UserMixin
from wtforms import RadioField
from wtforms.validators import InputRequired
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db= SQLAlchemy()

class UserData(db.Model, UserMixin):

    __name__ = 'user_data'

    id= Column(Integer, primary_key=True)
    username = Column(String(22))
    email = Column(String(22), unique=True, nullable=False)
    password = Column(String(22), nullable=False)
    blog = db.relationship('BlogData', backref=db.backref('user_data', uselist=False))
    # is_authenticated = Column(Boolean, default=False)
    # is_active= Column(Boolean, default=False)
    profile_pic= Column(String(120))

    # def get_reset_token(self, expires_sec=1800):
    #     s= Serializer(os.environ.get('SECRET_KEY') , expires_sec)
    #     return s.dumps({'user_id':self.id}).decode('utf-8')
    

    # @staticmethod
    # def verify_reset_token(token):
    #     s= Serializer(os.environ.get('SECRET_KEY'))
    #     try:
    #         user_id =s.loads(token)['user_id']
    #     except:
    #         return None
        
    #     return UserData.query.get(user_id)
    

    def __repr__(self) -> str:
        return f'<Id:{self.id}, Username:{self.username}, Email: {self.email}> '


class BlogData(db.Model):

    __name__='blog_data'

    id = Column(Integer, primary_key=True)
    writer_id = db.Column(db.Integer, ForeignKey('user_data.id')) 
    title = Column(String(22), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.date.today())
    blog_thumbnail = Column(String(120))
    category = Column(String(26))