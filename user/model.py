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
    name: string
    password: string
    email: string

    Methods
    ---
    create_user(first, last, password, email) -> Boolean Creates a user.
    login(email, pass) -> Boolean Logs user.
    logout() -> Logs user out.
    """

    __tablename__ = "User"
    name: Column[str] = Column(String)
    password: Column[str] = Column(String)
    email: Column[str] = Column(String, unique=True)

    def before_save(self):
        """Before saving the user encrypt the password."""
        self.password = sha256_crypt.hash(str(self.password))

    def verify(self, password: str) -> bool:
        """
        Check if password is correct or not.

        @param password `str`: the password that will be compared.
        @return boolean: true if they are the same.
        """
        if self.password is not None and password is not None:
            return sha256_crypt.verify(str(password), self.password)
        return False

    @staticmethod
    def find(email: str = "", id=None):
        """
        Find user with email.

        @param email `str`: Searchs using the email
        """
        if email != "":
            return (
                DbService.session.query(UserModel)
                .filter(UserModel.email.like(email))
                .all()
            )
        if id is not None:
            return (
                DbService.session.query(UserModel)
                .filter(UserModel.id.like(id))
                .all()
            )
        return DbService.session.query(UserModel).all()
