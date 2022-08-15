"""Customers endpoint unit tests"""
from datetime import datetime
from random import choice, randint
from string import ascii_lowercase

from .mocks import MockCustomer
from .testcase import FacturapiTestCase, assert_property_in, assert_status


class TestCustomersEndpoint(FacturapiTestCase):
    """Customers endpoint Test Cases"""

    mock_customer = MockCustomer()
    endpoint = "customers"

    def test_crud(self):
        """Test complete CRUD"""

        # Create test
        endpoint = self._get_endpoint(self.endpoint)
        mock_customer = self.mock_customer._asdict()
        new_customer = endpoint.create(mock_customer)

        assert_status(endpoint.last_status, endpoint.STATUS_CREATED)
        assert_property_in("id", new_customer)

        customer_id = new_customer["id"]

        # Retrieve test
        retrieved_customer = endpoint.retrieve(customer_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("id", retrieved_customer)

        # Update test
        username = "".join(choice(ascii_lowercase) for i in range(randint(5, 15)))
        fake_email = f"{username}@example.com"
        modified_data = {"email": fake_email, **mock_customer}
        updated_customer = endpoint.update(customer_id, modified_data)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert updated_customer["email"] == fake_email

        # Validation test
        validation_result = endpoint.validate(customer_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("is_valid", validation_result)

        # Deletion test
        endpoint.delete(customer_id)
        assert_status(endpoint.last_status, endpoint.STATUS_OK)

    def test_get_all_customers(self):
        """Get all customers"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all()

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_search_customers(self):
        """Search customers"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(search=self.mock_customer.tax_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_get_customers_created_last_year(self):
        """Get all customers created last year"""
        endpoint = self._get_endpoint(self.endpoint)
        today = datetime.today()
        last_january = today.replace(year=today.year - 1, month=1, day=1)
        last_december = today.replace(year=today.year - 1, month=12, day=31)
        result = endpoint.all(start_date=last_january, end_date=last_december)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_get_customers_first_page(self):
        """Get first page of customers limited by 5"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(page=1, limit=5)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)
