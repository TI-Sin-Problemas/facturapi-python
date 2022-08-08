"""Customers endpoint unit tests"""
from datetime import datetime
from random import choice, randint
from string import ascii_lowercase

from tests.mocks import MockCustomer
from tests.testcase import FacturapiTestCase


class TestCustomersEndpoint(FacturapiTestCase):
    """Customers endpoint Test Cases"""

    mock_customer = MockCustomer()

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.customers

    def _get_customer_id(self):
        """Returns mock customer ID"""
        return self.endpoint.all(search=self.mock_customer.tax_id)["data"][0]["id"]

    def test_create_customer(self):
        """Create customer"""
        customer = self.mock_customer._asdict()

        result = self.endpoint.create(customer)
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertIn(status, [self.endpoint.STATUS_CREATED, self.endpoint.STATUS_OK])

    def test_get_all_customers(self):
        """Get all customers"""
        result = self.endpoint.all()
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_search_customers(self):
        """Search customers"""
        result = self.endpoint.all(search=self.mock_customer.tax_id)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_customers_created_last_year(self):
        """Get all customers created last year"""
        today = datetime.today()
        last_january = today.replace(year=today.year - 1, month=1, day=1)
        last_december = today.replace(year=today.year - 1, month=12, day=31)
        result = self.endpoint.all(start_date=last_january, end_date=last_december)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_customers_first_page(self):
        """Get first page of customers limited by 5"""
        result = self.endpoint.all(page=1, limit=5)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_retrieve_customer_object(self):
        """Retrieve customer"""
        customer_id = self._get_customer_id()
        result = self.endpoint.retrieve(customer_id)
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_update_customer(self):
        """Update customer"""
        mock_customer = self.mock_customer
        customer_id = self._get_customer_id()
        username = "".join(choice(ascii_lowercase) for i in range(randint(5, 15)))
        fake_email = f"{username}@example.com"
        modified_data = {"email": fake_email, **mock_customer._asdict()}

        result = self.endpoint.update(customer_id, modified_data)
        status = self.endpoint.last_status

        self.assertEqual(result["email"], fake_email)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_customer_validation(self):
        """Validate customer fiscal information"""
        customer_id = self._get_customer_id()

        result = self.endpoint.validate(customer_id)
        status = self.endpoint.last_status

        self.assertIn("is_valid", result)
        self.assertEqual(200, status)

    def test_delete_customer(self):
        """Delete customer"""
        customer_id = self._get_customer_id()

        self.endpoint.delete(customer_id)
        status = self.endpoint.last_status
        expected_status = [self.endpoint.STATUS_OK, self.endpoint.STATUS_CONFLICT]
        self.assertIn(status, expected_status)
