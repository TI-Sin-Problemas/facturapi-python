"""Customers endpoint unit tests"""
from datetime import datetime
from unittest import TestCase
import settings

from src.facturapi import Facturapi


class FacturapiTestCase(TestCase):
    """Base Facturapi Test Case"""

    api = Facturapi(settings.FACTURAPI_KEY)


class TestCustomersEndopint(FacturapiTestCase):
    """Customers endpoint Test Cases"""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.customers

    def test_create_customer(self):
        """Create customer"""
        address = {"zip": "01000"}
        customer = {
            "legal_name": "Publico General",
            "tax_id": "XAXX010101000",
            "tax_system": "601",
            "address": address,
        }

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
        result = self.endpoint.all(search="Publico")
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

    def test_get_first_customer(self):
        """Get details of first customer in list"""
        data = self.endpoint.all()["data"]
        customer_id = data[0]["id"]
        result = self.endpoint.retrieve(customer_id)
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)
