import os

from dotenv import load_dotenv, find_dotenv
load_dotenv()
os.environ['APP_SETTINGS'] = 'app.config.TestingConfig'
os.environ['DATABASE_URL'] = 'postgresql+psycopg2://teste:teste@localhost/teste'
