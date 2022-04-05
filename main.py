"""Main."""

from sqlalchemy.sql.schema import MetaData
from db import DbService
from user import UserModel, create_user
from product import ProductModel, create_product


def init():
    """Start required services."""
    DbService.connect()


def main():
    """Func."""
    init()
    # prd = product.create_product("test", 30.5)
    # usr = user.create_user("test", "test last", "1234", "test@mail.com")
    DbService.create_tables()
    # usr.save()
    #
    # prd.save()


if __name__ == "__main__":
    main()
