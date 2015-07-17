import os
import logging
import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, request, session, g, redirect, abort
from flask_restful import Resource

from app import db, api, app
from models import Unit

log = logging.getLogger(__name__)

class UnitsEndpoint(Resource):
    def get(self):
        return [{'id': unit.id, 'name': unit.name} for unit in db.session.query(Unit).all()]

api.add_resource(UnitsEndpoint, '/api/v1/unit')