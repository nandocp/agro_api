# Mainly database integrity tests

from agro_api.entities.estate import EstateKind
from tests.factories.estates import EstateFactory


def test_is_urban_true_with_periurban(session):
    estate = EstateFactory(kind=EstateKind.periurban)

    assert estate.is_urban()


def test_is_urban_true_with_intraurban(session):
    estate = EstateFactory(kind=EstateKind.intraurban)

    assert estate.is_urban()


def test_is_urban_false(session):
    estate = EstateFactory(kind=EstateKind.rural)

    assert not estate.is_urban()

# def test_registry_codes_constraint(session):
#     """Test that registry_codes validation works at DB level"""
#     estate = Estate(account_id=account.id, label="Test", slug="test")

#     # Should accept NULL
#     estate.registry_codes = None
#     session.add(estate)
#     session.commit()  # Should succeed

#     # Should accept valid object
#     estate.registry_codes = {"car": "123"}
#     session.commit()  # Should succeed

#     # Should reject array
#     estate.registry_codes = ["car", "123"]
#     with pytest.raises(IntegrityError):
#         session.commit()
#     session.rollback()

#     # Should reject empty string key
#     estate.registry_codes = {"": "value"}
#     with pytest.raises(IntegrityError):
#         session.commit()

# def test_registry_codes_mutation(db_session):
#     """Verify MutableDict tracks in-place changes"""
#     estate = Estate(account_id=account.id, label="Test", slug="test")
#     estate.registry_codes = {"car": "123"}
#     db_session.add(estate)
#     db_session.commit()

#     # Modify in-place
#     estate.registry_codes["ccir"] = "456"
#     db_session.commit()  # Should detect change and update

#     updated = db_session.get(Estate, estate.id)
#     assert updated.registry_codes == {"car": "123", "ccir": "456"}

# def test_account_slug_uniqueness(db_session):
#     """Verify composite unique constraint works"""
#     account = Account(...)  # create account

#     Estate(account_id=account.id, label="Test", slug="same")
#     db_session.commit()

#     # Same slug, same account - should fail
#     with pytest.raises(IntegrityError):
#         Estate(account_id=account.id, label="Test2", slug="same")
#         db_session.commit()

#     # Same slug, different account - should succeed
#     account2 = Account(...)
#     Estate(account_id=account2.id, label="Test3", slug="same")
#     db_session.commit()  # Should work

# def test_account_delete_cascade(db_session):
#     """Verify ondelete='CASCADE' works"""
#     account = Account(...)
#     estate = Estate(account_id=account.id, label="Test", slug="test")
#     db_session.commit()

#     db_session.delete(account)
#     db_session.commit()

#     # Estate should be gone
#     assert db_session.get(Estate, estate.id) is None
