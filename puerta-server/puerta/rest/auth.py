import os
import logging
import datetime

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, request, session, g, redirect, abort
from flask_restful import Resource

from puerta.app import db, api, app
from puerta.models import User

log = logging.getLogger(__name__)

class AuthEndpoint(Resource):
    def post(self):
        '''
        Authenticate...
        '''
        j = request.get_json()
        try:
            user = db.session.query(User).filter(and_(
                            User.email == j.get('email'),
                            User.approved == True
                            )).one()
        except NoResultFound:
            abort(404)

        if user.check_password(j.get('pass')):
            session['user_id'] = user.id
            return {
                'id': user.id,
                'fullname': user.fullname,
                'role': user.role
            }
        
        abort(401)

    def delete(self):
        '''
        Remove authentication...
        '''
        session.pop('user_id', None)
        return {'success': True}

api.add_resource(AuthEndpoint, '/api/v1/auth')