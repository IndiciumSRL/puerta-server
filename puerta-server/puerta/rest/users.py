import logging

from flask import Flask, request, session, g, redirect, abort

from puerta.app import db, api, app
from puerta.models import User
from puerta.lib.auth import Resource

log = logging.getLogger(__name__)

class UsersEndpoint(Resource):
    def get(self):
        return [{
            'id': user.id,
            'fullname': user.fullname,
            'email': user.email,
            'created': user.created.isoformat(),
            'role': user.role,
            'approved': user.approved,
            'who_approved': user.who_approved,
            'children': [{
                    "fullname": child.fullname,
                    "unit": child.unit.name
                } for child in user.children]
            } for user in db.session.query(User).all()]

class UserEndpoint(Resource):
    def delete(self, id):
        user = db.session.query(User).get(id)        
        if user is None:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return {
            'success': True,
            'id': id}

    def post(self, id):
        '''
            Approve user
        '''
        user = db.session.query(User).get(id)        
        if user is None:
            abort(404)

        user.approved = not user.approved
        if user.approved:
            current_user = db.session.query(User).get(session['user_id'])
            if current_user:
                user.who_approved = current_user.fullname
            else:
                abort(403)

        db.session.commit()
        return {
            'success': True,
            'id': id}

    def put(self, id):
        user = db.session.query(User).get(id)        
        if user is None:
            abort(404)

        j = request.get_json()
        user.role = j.get('role')
        db.session.commit()
        return {
            'success': True,
            'id': id}

api.add_resource(UsersEndpoint, '/api/v1/user')
api.add_resource(UserEndpoint, '/api/v1/user/<int:id>')