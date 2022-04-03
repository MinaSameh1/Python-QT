"""Main."""

from sqlalchemy.sql.schema import MetaData
from db import DbService
import user


def init():
    db = DbService.get_instance()
    DbService.connect()
    MetaData().create_all(DbService.engine)


def main():
    """Func."""
    init()
    usr = user.create_user("test", "test last", "1234", "test@mail.com")
    usr.save()

    print(usr)


if __name__ == "__main__":
    main()
