import os
import logging
import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, request, session, g, redirect, abort
from flask_restful import Resource

from puerta.app import db, api, app
from puerta.models import User, Child

log = logging.getLogger(__name__)

class RegisterEndpoint(Resource):
    def post(self):
        '''
        Register a new user
        '''
        j = request.get_json()
        user = User(j.get('fullname'), j.get('email'), j.get('password'), j.get('subscribed'))
        db.session.add(user)

        for child in j.get('children'):
            dbChild = Child(child.get('fullname'))
            dbChild.unit_id = child.get('unitId')
            user.children.append(dbChild)

        db.session.commit()
        return {'success': True, 'id': user.id}

api.add_resource(RegisterEndpoint, '/api/v1/register')