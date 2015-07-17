import os
import logging
import datetime

from werkzeug import secure_filename
from flask import Flask, request, session, g, redirect, abort

from app import db, api, app
from models import Album, PhotoFile, User
from lib.auth import Resource

log = logging.getLogger(__name__)

class AlbumsEndpoint(Resource):
    def get(self):
        response = []
        for album in db.session.query(Album).all():
            cover = album.photos[0].id if album.photos.count() != 0 else None
            likes = 0
            for photo in album.photos:
                if likes < photo.user_likes.count():
                    cover = photo.id
            response.append({
                'id': album.id,
                'title': album.title,
                'description': album.description,
                'created': album.created.isoformat(),
                'coverUrl': cover,
                'photoCount': album.photos.count()
            })
        return response

    def post(self):
        '''
        Create a new album
        '''
        j = request.get_json()
        album = Album(j.get('title'), j.get('description'))
        db.session.add(album)
        db.session.commit()
        return {'success': True, 'id': album.id}

class AlbumEndpoint(Resource):
    def get(self, id):
        album = db.session.query(Album).get(id)
        if album is None:
            abort(404)

        user = db.session.query(User).get(session.get('user_id'))
        if not user:
            abort(403)
        
        return {
            'id': album.id,
            'title': album.title,
            'description': album.description,
            'created': album.created.isoformat(),
            'photos': [{
                'id': photo.id,
                'created': photo.created.isoformat(),
                'liked': photo in user.likes,
                'likes_count': photo.user_likes.count(),
                'comments_count': photo.comments.count(),
                'user': {'fullname': photo.user.fullname if photo.user else None}
            } for photo in album.photos]
        }

    def post(self, id):
        '''
            Upload a photo
        '''
        if not request.files:
            abort(422)

        album = db.session.query(Album).get(id)
        if album is None:
            abort(404)

        user = db.session.query(User).get(session.get('user_id'))
        if user is None:
            abort(403)
        
        file = request.files['file']
        filename = secure_filename(file.filename)
        try:
            os.makedirs(os.path.join(os.path.join(app.config['PHOTO_PATH'], str(album.id))))
        except:
            log.exception('What the hell?')
        file.save(os.path.join(os.path.join(app.config['PHOTO_PATH'], str(album.id)), filename))
        photo = PhotoFile(filename)
        photo.user = user
        album.photos.append(photo)
        db.session.commit()
        return {'success': True, 'id': album.id}

api.add_resource(AlbumsEndpoint, '/api/v1/album')
api.add_resource(AlbumEndpoint, '/api/v1/album/<int:id>')