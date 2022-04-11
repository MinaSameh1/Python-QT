"""Responsible for products related operations."""

from .model import ProductModel
import logging


def create_product(
    product_name: str, product_price: float
) -> ProductModel or None:
    """
    Create Product.

    @param product_name `str`: The product's name
    @param product_price `str`: The product's price

    @return ProductModel, None if failed and Object if success
    """
    product = ProductModel(
        product_name=product_name, product_price=product_price
    )
    try:
        product.save()
        return product
    except Exception as err:
        logging.error(err)
        return None


def update_product(product_name, product_price, product_id=None) -> bool:
    """Update Product in db by name or ID."""
    if id is not None:
        product = ProductModel.find(product_id=product_id)
    else:
        product = ProductModel.find(product_name=product_name)
    product[0].product_name = product_name
    product[0].product_price = product_price
    try:
        product[0].update()
        return True
    except Exception as err:
        logging.error(err)
        return False


def delete_product(product_name: str, product_id=None):
    """Delete Product by name or id."""
    product = ProductModel.find(product_name, product_id=product_id)
    try:
        product[0].delete()
        return True
    except Exception as err:
        logging.error(err)
        return False


def get_products(name=""):
    """Get Products, if name is not set return all."""
    return ProductModel.find(name)
