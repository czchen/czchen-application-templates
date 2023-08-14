#!/usr/bin/env python3
import http
import logging
import logging.config
import pathlib
import time

from omegaconf import OmegaConf
from werkzeug.exceptions import NotFound
import connexion
import hydra
import prance


from .storages import db


def load_config_and_get_flask_app():
    hydra.initialize(version_base=None, config_path='../conf')
    return get_flask_app()


def get_bundled_spec():
    parser = prance.ResolvingParser(
        str((pathlib.Path(__file__).parent.parent / 'openapi' / 'main.yml').absolute()),
        lazy=False,
        backend='openapi-spec-validator'
    )
    parser.parse()
    return parser.specification


def get_flask_app():
    config = OmegaConf.to_container(hydra.compose(config_name='config'))

    logging.Formatter.converter = time.gmtime
    logging.config.dictConfig(config['logging'])

    connextion_app = connexion.FlaskApp(
        __name__,
        specification_dir='openapi/',
        options={
            'swagger_ui': True,
        },
    )

    connextion_app.add_api(
        get_bundled_spec(),
        strict_validation=True,
        validate_responses=True,
    )

    flask_app = connextion_app.app

    flask_app.config.update(config['app']['config'])
    db.init_app(flask_app)

    ###########################################################################
    # Setup handlers
    ###########################################################################

    @flask_app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Headers'] = 'authorization,content-type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


    @flask_app.errorhandler(NotFound)
    def handle_bad_request(exc):
        res = {
            'title': http.HTTPStatus.NOT_FOUND.phrase,
            'type': '',
            'detail': f'exc = {exc}',
            'status': http.HTTPStatus.NOT_FOUND,
        }
        logging.warning(f'{res=}')
        return res, res['status']

    return flask_app
