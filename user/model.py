"""Model of User SQLite Interface."""

from dataclasses import dataclass

from passlib.hash import sha256_crypt

from sqlalchemy import Column, String
from db import BaseModel, DbService


__all__ = ["UserModel"]


@dataclass(init=True)
class UserModel(BaseModel):
    """
    UserModel Class, used with SqlAlchemy ORM and sqlite.

    Attribuites
    ---
    user_id: int
    first_name: string
    last_name: string
    password: string
    email: string

    Methods
    ---
    create_user(first, last, password, email) -> Boolean Creates a user.
    login(email, pass) -> Boolean Logs user.
    logout() -> Logs user out.
    """

    __tablename__ = "User"
    first_name: Column = Column(String)
    last_name: Column = Column(String)
    password: Column = Column(String)
    email: Column = Column(String, unique=True)

    def before_save(self) -> None:
        """Before saving the user encrypt the password."""
        self.password = sha256_crypt.hash(str(self.password))

    def verify(self, password: str) -> bool:
        """
        Check if password is correct or not.

        @param password `str`: the password that will be compared.
        @return boolean: true if they are the same.
        """
        return sha256_crypt.verify(password, self.password)

    @staticmethod
    def find(email):
        """
        Find user with email.

        @param email `str`: Searchs using the email
        """
        return (
            DbService.session.query(UserModel)
            .filter(UserModel.email.like(email))
            .all()
        )
