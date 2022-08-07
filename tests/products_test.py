"""Products endpoint unit tests"""
from typing import NamedTuple
from tests.testcase import FacturapiTestCase


class MockProduct(NamedTuple):
    """Mock product class"""

    description: str
    product_key: str
    price: float


class TestProductsEndpoint(FacturapiTestCase):
    """Products endpoint Test Cases"""

    product = MockProduct("Ukulele", "60131324", 345.6)

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.products

    def test_create_product(self):
        """Create product"""
        product = self.product._asdict()
        result = self.endpoint.create(product)
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertIn(status, [self.endpoint.STATUS_CREATED, self.endpoint.STATUS_OK])

    def test_get_all_products(self):
        """Get all products"""
        result = self.endpoint.all()
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_search_products(self):
        """Search products"""
        result = self.endpoint.all(search=self.product.description)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_limited_products_by_page(self):
        """Get first page of products limited by 5"""
        result = self.endpoint.all(page=1, limit=5)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)
