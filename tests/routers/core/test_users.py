# from http import HTTPStatus
# from secrets import token_hex

# import pytest
# from sqlalchemy import select

# from agro_api.entities.core import User
# from tests.factories.core import UserFactory


# # @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_create_new_user(client, session, mock_id):
#     new_user = UserFactory()
#     user_data = {
#         'name': new_user.name,
#         'email': new_user.email,
#         'password': token_hex(4),
#     }

#     user_db = await session.scalar(
#         select(User).where(User.email == user_data['email'])
#     )

#     assert not user_db

#     response = client.post('/users', json=user_data)
#     user_db = await session.scalar(
#         select(User).where(User.email == user_data['email'])
#     )

#     assert user_db
#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == {
#         'id': str(user_db.id),
#         'created_at': str(user_db.created_at).replace(' ', 'T'),
#         'updated_at': str(user_db.updated_at).replace(' ', 'T'),
#         'email': user_db.email,
#         'last_sign_in_at': str(user_db.last_sign_in_at).replace(' ', 'T'),
#         'current_sign_in_at': str(user_db.current_sign_in_at).replace(
#             ' ', 'T'
#         ),
#         'is_active': True,
#         'name': user_db.name,
#     }


# # @pytest.mark.skip
# def test_create_existing_user(client):
#     pwd = token_hex(4)
#     user = UserFactory.build()
#     user_data = {'name': user.name, 'email': user.email, 'password': pwd}
#     original_response = client.post('/users', json=user_data)
#     assert original_response.status_code == HTTPStatus.CREATED

#     test_response = client.post('/users', json=user_data)
#     assert test_response.status_code == HTTPStatus.CONFLICT


# # @pytest.mark.skip
# def test_show_user_with_auth(client, session, token, user):
#     response = client.get(
#         f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
#     )

#     columns = [
#         'id',
#         'created_at',
#         'updated_at',
#         'name',
#         'email',
#         'last_sign_in_at',
#         'current_sign_in_at',
#         'is_active',
#     ]
#     assert response.status_code == HTTPStatus.OK
#     assert list(response.json().keys()) == columns


# # @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_show_another_user_with_auth(client, session, token):
#     user = UserFactory.create()
#     session.add(user)
#     await session.commit()

#     response = client.get(
#         f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
#     )

#     assert response.status_code == HTTPStatus.UNAUTHORIZED


# # @pytest.mark.skip
# def test_show_user_without_auth(client, user):
#     response = client.get(f'/users/{user.id}')
#     assert response.status_code == HTTPStatus.UNAUTHORIZED


# # @pytest.mark.skip
# def test_put_update_user(client, user, token):
#     new_user = UserFactory()
#     new_data = {
#         'name': new_user.name,
#         'email': new_user.email,
#         'password': token_hex(6),
#     }

#     assert user.name != new_data['name']

#     response = client.put(
#         f'/users/{user.id}',
#         json=new_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.OK
#     assert user.name == new_data['name']
