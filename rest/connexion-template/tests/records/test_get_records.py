import http

from app.storages import db
from app.storages import Record


def test_get_record_found(setup_app):
    test_client = setup_app['test_client']

    record_name = 'record-name'

    record = Record(
        name='record-name',
    )

    db.session.add(record)
    db.session.commit()

    rsp = test_client.get(f'records/{record.id}')

    assert rsp.status_code == http.HTTPStatus.OK
    assert rsp.json['record']['id'] == record.id
    assert rsp.json['record']['name'] == record_name


def test_get_record_not_found(setup_app):
    test_client = setup_app['test_client']

    rsp = test_client.get('records/0')

    assert rsp.status_code == http.HTTPStatus.NOT_FOUND
