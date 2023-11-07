#!/usr/bin/env python3
import http
import logging
import logging.config
import pathlib
import time

from connexion.options import SwaggerUIOptions
from omegaconf import OmegaConf
from werkzeug.exceptions import NotFound
import connexion
import hydra


from .storages import db


def load_config_and_get_app():
    hydra.initialize(version_base=None, config_path='../conf')
    return get_app()


def get_app():
    config = OmegaConf.to_container(hydra.compose(config_name='config'))

    logging.Formatter.converter = time.gmtime
    logging.config.dictConfig(config['logging'])

    connextion_app = connexion.FlaskApp(
        __name__,
        specification_dir='openapi/',
        swagger_ui_options=SwaggerUIOptions(swagger_ui=True)
    )

    connextion_app.add_api(
        (pathlib.Path(__file__).parent.parent / 'openapi' / 'main.yml').absolute(),
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
    def handle_not_found(exc):
        res = {
            'title': http.HTTPStatus.NOT_FOUND.phrase,
            'type': '',
            'detail': f'exc = {exc}',
            'status': http.HTTPStatus.NOT_FOUND,
        }
        logging.warning(f'{res=}')
        return res, res['status']

    return connextion_app
