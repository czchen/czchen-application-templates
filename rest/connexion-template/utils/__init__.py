import logging
import logging.config
import time

from flask import Flask
from flask_migrate import Migrate
from omegaconf import OmegaConf
import hydra

from app.storages import db


POSTGRES_IMAGE = 'docker.io/postgres:15.4-bookworm'


def get_migration_app():
    flask_app = Flask(__name__)

    hydra.initialize(version_base=None, config_path='../conf')
    config = OmegaConf.to_container(hydra.compose(config_name='config'))

    logging.Formatter.converter = time.gmtime
    logging.config.dictConfig(config['logging'])

    flask_app.config.update(config['app']['config'])

    db.init_app(flask_app)

    Migrate(flask_app, db)

    return flask_app
