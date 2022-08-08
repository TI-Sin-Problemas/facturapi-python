"""Products endpoint unit tests"""
from random import choice, randint
from string import ascii_lowercase
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

    def _get_product_id(self):
        """Returns mock product ID"""
        return self.endpoint.all(search=self.product.description)["data"][0]["id"]

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

    def test_retrieve_product(self):
        """Retrieve single product object"""
        result = self.endpoint.retrieve(self._get_product_id())
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_update_product(self):
        """Update product"""
        product = self.endpoint.retrieve(self._get_product_id())
        fake_sku = "".join(choice(ascii_lowercase) for i in range(randint(5, 10)))
        modified_data = {"sku": fake_sku, **self.product._asdict()}

        result = self.endpoint.update(product["id"], modified_data)
        status = self.endpoint.last_status

        self.assertEqual(result["sku"], fake_sku)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_delete_product(self):
        """Delete product"""
        product_id = self._get_product_id()
        result = self.endpoint.delete(product_id)
        status = self.endpoint.last_status

        self.assertEqual(product_id, result["id"])
        self.assertEqual(status, self.endpoint.STATUS_OK)
