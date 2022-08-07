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
