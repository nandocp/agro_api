from http import HTTPStatus

import pytest

from config.settings import settings


@pytest.mark.asyncio
async def test_root_response(client):
    response = await client.get('/')

    assert response.json() == {
        'message': 'AgroAPI',
        'version': settings.VERSION,
    }
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_up_response(client):
    response = await client.get('/up')

    assert response.json() == {'message': 'ok'}
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_html_response(client):
    response = await client.get('/html')

    assert (
        response.text
        == """<html>
        <head>AgroAPI</head>
        <body>🚜</body>
    </html>"""
    )
    assert response.status_code == HTTPStatus.OK
