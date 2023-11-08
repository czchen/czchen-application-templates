from collections import namedtuple
import pathlib

from testcontainers.postgres import PostgresContainer
import hydra
import pytest

from app.storages import db
import app
import utils


@pytest.fixture(scope='session', autouse=True)
def setup_app():
    config = pathlib.PosixPath(__file__).parent.parent / 'conf' / 'app' / 'override.yaml'
    App = namedtuple('App', ['app', 'db', 'test_client'])

    with PostgresContainer(utils.POSTGRES_IMAGE) as postgres:
        with config.open('wt') as f:
            f.write(f'''
config:
  SQLALCHEMY_DATABASE_URI: {postgres.get_connection_url()}''')
        hydra.initialize(version_base=None, config_path='../conf')

        connexion_app = app.get_app()

        with connexion_app.app.app_context():
            db.create_all()

            with db.engine.connect(), connexion_app.test_client() as test_client:
                yield App(
                    app=connexion_app,
                    db=db,
                    test_client=test_client,
                )


@pytest.fixture(scope='function', autouse=True)
def cleanup_datbase(setup_app):
    flask_app = setup_app.app.app

    with flask_app.test_request_context() as request_ctx:
        request_ctx.push()
        with flask_app.app_context():
            db.session.rollback()
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

            yield
