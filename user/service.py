"""Responsible for anything User related operations."""
import logging
from .model import UserModel


def create_user(
    name: str,
    email: str,
    password: str,
) -> UserModel or bool:
    """
    Create User.

    @param name `str`: Name of User.
    @param password `str`: password of User, will be encrypted.
    @param email `str`: Email of User

    @return UserModel, None if failed and Object if success
    """
    usr_exists = UserModel.find(email)
    if usr_exists:
        return False
    user = UserModel(name=name, password=password, email=email)
    try:
        user.save()
        return user
    except Exception as err:
        logging.error(err)
        return False


def login(email, password) -> UserModel or bool:
    """Login current user."""
    user = UserModel.find(email)
    if user is not None and len(user) > 0:
        if user[0].verify(password):
            return user[0]
    return False


def delete_user(email: str, user_id=None):
    """Delete user using Email."""
    if id is not None:
        user = UserModel.find(id=user_id)
    else:
        user = UserModel.find(email)
    if user is not None:
        return user.delete()
    return False


def update_user(user_id, email: str, name: str, password: str):
    """Update user using ID."""
    user = UserModel.find(id=user_id)
    user.update(email=email, name=name, password=password)
