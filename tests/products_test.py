"""Products endpoint tests"""
import random
import string

import pytest
from settings import API_KEY

from facturapi import Facturapi
from facturapi.models import Product, ProductList


class TestProducts:
    """Products tests group"""

    api = Facturapi(API_KEY)
    product = api.products.create("Product 1", "01010101", 100)

    def test_create_product(self):
        """Test product creation"""

        # Check if the result is a Product instance
        assert isinstance(self.product, Product)

    def test_get_all_products(self):
        """Test get all products"""
        products = self.api.products.all()

        # Check if the result is a ProductList instance
        assert isinstance(products, ProductList)

        # Check if all the items are Product instances
        assert all(isinstance(product, Product) for product in products)

    def test_search_products(self):
        """Test product search"""
        products = self.api.products.all(search=self.product.description)

        # Check if "Product 1" is in the result
        assert self.product.description in [product.description for product in products]

    @pytest.mark.skipif(not product, reason="Product creation failed")
    def test_retrieve_one_product(self):
        """Test get a product"""
        product = self.api.products.retrieve(self.product.id)

        # Check if the result is a Product instance
        assert isinstance(product, Product)

    @pytest.mark.skipif(not product, reason="Product creation failed")
    def test_update_product(self):
        """Test product update"""
        description = "A new product"
        price = 200
        letters = string.ascii_uppercase
        sku = "".join(random.choice(letters) for i in range(10))
        product = self.api.products.update(
            self.product.id, description=description, price=price, sku=sku
        )

        # Check if the result is correct
        assertions = [
            product.description == description,
            product.price == price,
            product.sku == sku,
        ]
        assert all(assertions)
