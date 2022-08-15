"""Products endpoint unit tests"""
from random import choice, randint
from string import ascii_lowercase

from tests.mocks import MockProduct
from tests.testcase import FacturapiTestCase, assert_property_in, assert_status


class TestProductsEndpoint(FacturapiTestCase):
    """Products endpoint Test Cases"""

    mock_product = MockProduct()
    endpoint = "products"

    def test_crud(self):
        """Test complete CRUD"""

        # Create test
        mock_product = self.mock_product._asdict()
        endpoint = self._get_endpoint(self.endpoint)
        new_product = endpoint.create(mock_product)

        assert_status(endpoint.last_status, endpoint.STATUS_CREATED)
        assert_property_in("id", new_product)

        product_id = new_product["id"]

        # Retrieve test
        retrieved_product = endpoint.retrieve(product_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("id", retrieved_product)

        # Update test
        fake_sku = "".join(choice(ascii_lowercase) for i in range(randint(5, 10)))
        modified_data = {"sku": fake_sku, **mock_product}
        updated_customer = endpoint.update(product_id, modified_data)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert updated_customer["sku"] == fake_sku

        # Delete test
        endpoint.delete(product_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)

    def test_get_all_products(self):
        """Get all products"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all()

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_search_products(self):
        """Search products"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(search=self.mock_product.description)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_get_limited_products_by_page(self):
        """Get first page of products limited by 5"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(page=1, limit=5)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)
