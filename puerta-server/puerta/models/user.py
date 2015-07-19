import datetime
import logging

import bcrypt

from puerta.app import db

log = logging.getLogger(__name__)

__all__ = ["User", "Child", "Unit"]

user_child = db.Table('user_child',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('child.id'))
)

photo_likes = db.Table('photo_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('photo_id', db.Integer, db.ForeignKey('photo_file.id'))
)

class User(db.Model):
    """Represents an user on the system"""
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Unicode(255), unique=False, nullable=False)
    email = db.Column(db.Unicode(255), unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    mail_notifications = db.Column(db.Boolean, unique=False, default=True)
    approved = db.Column(db.Boolean, unique=False, default=False)
    who_approved = db.Column(db.Unicode(255), unique=False, nullable=True)
    role = db.Column(db.Unicode(255), unique=False, nullable=False, default=u"guest")
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    children = db.relationship('Child', secondary=user_child, backref=db.backref('relatives', lazy='dynamic'))
    likes = db.relationship('PhotoFile', secondary=photo_likes, backref=db.backref('user_likes', lazy='dynamic'))

    def __init__(self, fullname, email, password, mail_notifications=True):
        self.fullname = fullname
        self.email = email
        self.password = self.hash_password(password)
        self.mail_notifications = mail_notifications

    def hash_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return (bcrypt.hashpw(password, self.password) == self.password)
        
class Child(db.Model):
    """Represents a child"""
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Unicode(255), unique=False, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unit = db.relationship('Unit', backref="children", cascade="save-update")

    def __init__(self, fullname):
        self.fullname = fullname
                        
class Unit(db.Model):
    """Represents a unit"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), unique=False, nullable=False)

    def __init__(self, name):
        self.name = name