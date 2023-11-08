import http


def test_read_info(setup_app):
    rsp = setup_app.test_client.get('info')
    assert rsp.status_code == http.HTTPStatus.OK
