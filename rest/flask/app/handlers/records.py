import http

from werkzeug.exceptions import NotFound

from app.storages import Records


def get_record(record_id):
    record = Records.query.filter(Records.id == record_id).first()
    if not record:
        raise NotFound(f'cannot find {record_id}')

    return {
        'record': {
            'id': record.id,
            'name': record.name,
        }
    }, http.HTTPStatus.OK,
