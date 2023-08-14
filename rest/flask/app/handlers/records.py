import http

from werkzeug.exceptions import NotFound

from app.storages import Record


def get_record(record_id):
    record = Record.query.filter(Record.id == record_id).first()
    if not record:
        raise NotFound(f'cannot find {record_id}')

    return {
        'record': {
            'id': record.id,
            'name': record.name,
        }
    }, http.HTTPStatus.OK,
