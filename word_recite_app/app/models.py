from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table for user ↔ word "notebook" relationship
notebook_table = Table(
    'notebook',
    db.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('word_id', Integer, ForeignKey('word.id'), primary_key=True),
    Column('added_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    interests = db.Column(db.String(256))  # stores comma-separated categories
    duration = db.Column(db.Integer)       # time to complete task
    unit = db.Column(db.String(10))        # 'days', 'weeks', or 'months'
    reminder = db.Column(Boolean, default=False)  # whether SMS reminders enabled
    phone = db.Column(db.String(20))       # user's phone number for SMS reminders

    # Relationship: words the user has added to their notebook
    notebook = relationship('Word', secondary=notebook_table, back_populates='fans')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(200), nullable=False)
    phonetic = db.Column(db.String(100))
    category = db.Column(db.String(64), default='all')

    # Back-reference: which users have this word in their notebook
    fans = relationship('User', secondary=notebook_table, back_populates='notebook')

class CheckIn(db.Model):
    __tablename__ = 'check_in'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow, unique=True)  # one check-in per day
