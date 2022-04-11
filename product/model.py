"""Model of Product SQLite Interface."""

from dataclasses import dataclass

from sqlalchemy import Column, String, Float, Integer, Table
from sqlalchemy.sql.schema import ForeignKey
from db import BaseModel, DbService


__all__ = ["ProductModel"]


@dataclass
class ProductModel(BaseModel):
    """
    ProductModel Class, used with SqlAlchemy ORM and sqlite.

    Attribuites
    ---
    product_name: `str` The name of the product.
    product_price: `float` The price of the product.
    """

    __tablename__ = "Products"
    product_name: Column = Column(String, unique=True)
    product_price: Column = Column(Float, nullable=False)

    @staticmethod
    def find(product_name: str = "", product_id=None):
        """
        Find Product with name

        @param name `str`: Searchs using product name
        @param id: Searching using ID
        """
        if product_id is not None:
            return (
                DbService.session.query(ProductModel)
                .filter(ProductModel.id.like(product_id))
                .all()
            )
        if product_name != "":
            return (
                DbService.session.query(ProductModel)
                .filter(ProductModel.product_name.like(product_name))
                .all()
            )
        return DbService.session.query(ProductModel).all()


# ProductCart = Table(
#     "Cart",
#     DbService.Base.metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_id", Integer, ForeignKey("User.id"), nullable=False),
# )
#
# ProductCartItem = Table(
#     "CartItem",
#     DbService.Base.metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("cart_id", Integer, ForeignKey("Cart.id"), nullable=False),
#     Column("ProductItem", Integer, ForeignKey("Products.id"), nullable=False),
# )
