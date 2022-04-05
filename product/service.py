"""Responsible for products related operations."""

from .model import ProductModel
import logging


def create_product(product_name: str, product_price: float) -> ProductModel:
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
