"""Products endpoint tests"""
from settings import API_KEY

from facturapi import Facturapi
from facturapi.models import Product


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

        # Get all products
        products = self.api.products.all()

        # Check if the result is a ProductList instance
        assert isinstance(products, ProductList)

        # Check if all the items are Product instances
        assert all(isinstance(product, Product) for product in products)

