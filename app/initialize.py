# -*- coding: utf-8 -*-
from app import config, api
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy

from app.infrastructure import database

web_app = Flask(__name__)
web_app.config.from_object(config)
database.AppRepository.db = SQLAlchemy(web_app)

api.create_api(web_app)


@web_app.after_request
def add_cache_header(response):
    """
    Add response headers for Cache Control
    """
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

