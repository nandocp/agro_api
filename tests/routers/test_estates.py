from http import HTTPStatus

from tests.factories.estates import EstateFactory


def test_create_estate(client, session, user, token):
    new_estate = EstateFactory(user_id=user.id)
    estate_data = {
        'slug': new_estate.slug,
        'label': new_estate.label,
        'opened_at': str(new_estate.opened_at),
        'kind': 'rural'
    }

    response = client.post(
        '/estates',
        json=estate_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.CREATED
    # assert response.json() == {
    #     'name': user_data['name'],
    #     'email': user_data['email'],
    #     'id': str(user_db.id),
    #     'created_at': str(user_db.created_at).replace(' ', 'T'),
    # }
