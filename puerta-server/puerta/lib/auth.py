import logging
from functools import wraps

from flask_restful import Resource, abort
from flask import request, session

log = logging.getLogger(__name__)

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)

        log.warning('Trying to access something wrong...')

        abort(401)
    return wrapper


class Resource(Resource):
    method_decorators = [authenticate]   # applies to all inherited resources