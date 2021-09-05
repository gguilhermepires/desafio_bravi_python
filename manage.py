#! /usr/bin/env python
# -*- coding: utf-8 -*-
# utilizado no teste
import os
# from dotenv import load_dotenv
#
# base_path = os.path.dirname(__file__)
# base_path = base_path.replace('/tests/integration', '')
# base_path = base_path.replace('/app', '')
# if not os.path.isfile(f'{base_path}/.env'):
#     raise Exception(f"env not exist path={base_path}/.env")
# load_dotenv(verbose=True, dotenv_path=os.path.join(base_path, '.env'))


import sys
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import initialize
from app.repositories import *

manager = Manager(initialize.web_app)


def register_migrate(manager):
    migrate = Migrate(initialize.web_app, db)
    manager.add_command('db', MigrateCommand)
    return migrate


if __name__ == '__main__':
    if 'db' in sys.argv:
        migrate = register_migrate(manager)
    manager.run()
