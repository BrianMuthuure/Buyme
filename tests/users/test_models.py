import pytest


def test_user_str(user):
    assert user.__str__() == user.email


def test_user_get_full_name(user):
    assert user.get_full_name() == f"{user.first_name} {user.last_name}"


def test_user_get_short_name(user):
    assert user.get_short_name() == user.first_name


def test_user_has_perm(user):
    assert user.has_perm("perm", "obj") == True


def test_user_has_module_perms(user):
    assert user.has_module_perms("app_label") == True


def test_user_email_is_normalized(user):
    assert user.email == user.email.lower()


def test_super_user_email_is_normalized(super_user):
    assert super_user.email == super_user.email.lower()


def test_super_user_not_staff(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(error.value) == "Superuser must have staff=True."


def test_super_user_not_admin(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(error.value) == "Superuser must have admin=True."


def test_create_user_no_first_name(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(first_name=None)
    assert str(error.value) == "User must have a first name"


def test_create_user_no_last_name(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(last_name=None)
    assert str(error.value) == "User must have a last name"


def test_create_user_no_email(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(email=None)
    assert str(error.value) == "User must have an email address"


def create_super_user_no_password(user_factory):
    with pytest.raises(ValueError) as error:
        user_factory.create(is_superuser=True, is_staff=True, password=None)
    assert str(error.value) == "Superuser must have a password."
