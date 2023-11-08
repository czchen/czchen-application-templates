import http

from app.storages import Record


def test_read_record_found(setup_app):

    record_name = 'record-name'

    record = Record(
        name='record-name',
    )

    setup_app.db.session.add(record)
    setup_app.db.session.commit()

    rsp = setup_app.test_client.get(f'records/{record.id}')

    assert rsp.status_code == http.HTTPStatus.OK

    body = rsp.json()
    assert body['record']['id'] == record.id
    assert body['record']['name'] == record_name


def test_read_record_not_found(setup_app):
    rsp = setup_app.test_client.get('records/0')

    assert rsp.status_code == http.HTTPStatus.NOT_FOUND
