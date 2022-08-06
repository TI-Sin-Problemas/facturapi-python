"""Customers endpoint unit tests"""
import unittest
import settings

from src.facturapi import Facturapi


class FacturapiTestCase(unittest.TestCase):
    """Base Facturapi Test Case"""

    api = Facturapi(settings.FACTURAPI_KEY)


class TestCustomersEndopint(FacturapiTestCase):
    """Customers endpoint Test Cases"""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.customers

    def test_create_customer(self):
        """Create customer Test Case"""
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
        self.assertIn(status, [200, 201])
