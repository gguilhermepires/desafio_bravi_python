from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy

import config, api
from infrastructure import database


web_app = Flask(__name__)
web_app.config.from_object(config)
database.AppRepository.db = SQLAlchemy(web_app)

api.create_api(web_app)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'



# if __name__ == '__main__':
#     app.run()
