#! /usr/bin/env python

import os

from flask_script import Manager

from comma_api import create_app, db


app = create_app(os.getenv('COMMA_API_CONFIG', 'default'))
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
