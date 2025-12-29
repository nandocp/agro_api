"""
3  steps tests:
- Arrange: configurations (what is needed)
- Act: calls the block code to be tested
- Assert: guarantees that something is working as it should be
"""

from http import HTTPStatus

from config.settings import settings


def test_root_response(client):
    response = client.get('/')

    assert response.json() == {
        'message': 'AgroAPI',
        'version': settings.VERSION,
    }
    assert response.status_code == HTTPStatus.OK


def test_up_response(client):
    response = client.get('/up')

    assert response.json() == {'message': 'ok'}
    assert response.status_code == HTTPStatus.OK


def test_html_response(client):
    response = client.get('/html')

    assert (
        response.text
        == """<html>
        <head>AgroAPI</head>
        <body>🚜</body>
    </html>"""
    )
    assert response.status_code == HTTPStatus.OK
