from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import psycopg2

from config import config


db = SQLAlchemy()
ma = Marshmallow()

def new_db_conn():
    try:
        print config['default'].DB_NAME
        conn = psycopg2.connect("dbname='%s' user='%s'" % (config['default'].DB_NAME, config['default'].DB_USER))
        return conn
    except:
        print "Cannot establish connection to Postgres"


def get_db_conn():
    if conn.status == psycopg2.extensions.STATUS_READY or conn.status == psycopg2.extensions.STATUS_BEGIN:
        return conn
    else:
        print "making new db connection"
        return new_db_conn()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app)
    db.init_app(app)
    ma.init_app(app)

    from api import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app

conn = new_db_conn()