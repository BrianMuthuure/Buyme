import pytest
from pytest_factoryboy import register

from .tests.factories import (UserFactory)

register(UserFactory)


@pytest.fixture
def user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def super_user(db, user_factory):
    user = user_factory.create(staff=True, is_superuser=True)
    return user