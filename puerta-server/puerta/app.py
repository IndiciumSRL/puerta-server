import sys
import logging
import os

from flask import Flask, request, session, g, redirect, abort
from flask import send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from custom_session import ItsdangerousSessionInterface


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

# configuration
DEBUG = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['PHOTO_PATH'] = '/tmp/photos'
app.session_interface = ItsdangerousSessionInterface()
db = SQLAlchemy(app)
api = Api(app)

from puerta.rest import *
from puerta.models import *

if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    
    if len(sys.argv)>1:
        print 'This is lazy loading?'
        db.create_all()
        u = User(u'Admin', u'admin@admin.com', u'admin')
        u.role = u'admin'
        u.approved = True
        u.who_approved = u'Admin'
        db.session.add(u)

        for unit in [u'Nido', u'Prisma', u'Puerta']:
            db.session.add(Unit(unit))

        db.session.commit()
        sys.exit(0)
    
    app.run('0.0.0.0', port=8081)