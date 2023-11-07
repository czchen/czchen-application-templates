import http


def get_info():
    return {
        'version': '0.0.0',
    }, http.HTTPStatus.OK
