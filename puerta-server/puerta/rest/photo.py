import os
import logging
import datetime

from flask import send_from_directory
from flask import Flask, request, session, g, redirect, abort

from puerta.models.user import User
from puerta.models.album import PhotoFile
from puerta.app import app, db, api
from puerta.lib.auth import Resource

log = logging.getLogger(__name__)

class PhotoEndpoint(Resource):
    def get(self, id):
        photo = db.session.query(PhotoFile).get(id)
        if photo is None:
            abort(404)

        return send_from_directory(os.path.join(app.config['PHOTO_PATH'],
            str(photo.album.id)), photo.filename)

    def post(self, id):
        photo = db.session.query(PhotoFile).get(id)
        if photo is None:
            abort(404)

        user = db.session.query(User).get(session.get('user_id'))
        if user is None:
            abort(403)

        if photo in user.likes:
            user.likes.remove(photo)
            liked = False
        else:
            user.likes.append(photo)
            liked = True
        db.session.commit()
        return {'success': True, 'likes_count': photo.user_likes.count(), 'liked': liked}

class PhotoCommentEndpoint(Resource):
    def get(self, id):
        '''
        id is the photo id...
        '''
        photo = db.session.query(PhotoFile).get(id)
        if photo is None:
            abort(404)

        return {
            'photo_id': photo.id,
            'comments': [{
                'id': comment.id,
                'comment': comment.comment
            } for comment in photo.comments]
        }
        

api.add_resource(PhotoCommentEndpoint, '/api/v1/album/photo/<int:id>/comment')
api.add_resource(PhotoEndpoint, '/api/v1/album/photo/<int:id>')