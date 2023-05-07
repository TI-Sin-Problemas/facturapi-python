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
