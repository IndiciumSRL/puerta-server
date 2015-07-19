import datetime
import logging

from puerta.app import db

log = logging.getLogger(__name__)

__all__ = ["Album", "PhotoFile", "Comment"]

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), unique=True, nullable=False)
    description = db.Column(db.Unicode(255), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    photos = db.relationship('PhotoFile', backref='album', cascade='delete,delete-orphan,save-update', lazy="dynamic")

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Album %r>' % self.title


class PhotoFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=False, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="uploaded_photos")

    def __init__(self, filename):
        self.filename = filename

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Unicode, unique=False, nullable=False)
    photo_file_id = db.Column(db.Integer, db.ForeignKey('photo_file.id'), nullable=False)
    photo = db.relationship('PhotoFile', backref=db.backref("comments", lazy="dynamic"), cascade="delete,delete-orphan,save-update", single_parent=True)