"""Responsible for anything User related operations."""
import logging
from .model import UserModel


def create_user(first: str, last: str, password: str, email: str) -> UserModel:
    """
    Create User.

    @param first `str`: First name of User.
    @param last `str`: Last name of User.
    @param password `str`: password of User, will be encrypted.
    @param email `str`: Email of User

    @return UserModel, None if failed and Object if success
    """
    user = UserModel(
        first_name=first, last_name=last, password=password, email=email
    )
    try:
        user.save()
        return user
    except Exception as err:
        logging.error(err)
        return None


def login(email, password) -> UserModel or bool:
    """Login current user."""
    user = UserModel.find(email)
    if user is not None:
        if user[0].verify(password):
            return user
    return False
