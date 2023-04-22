"""Customers endpoint tests"""
from settings import API_KEY

from facturapi import Facturapi
from facturapi.constants import TaxSystem
from facturapi.models import Customer, CustomerList


class TestCustomers:
    """Test case for getting all the customers"""

    customers = Facturapi(API_KEY).customers

    def test_create_customer(self):
        """Test for customer creation"""
        result = self.customers.create(
            "PÚBLICO EN GENERAL",
            "XAXX010101000",
            TaxSystem.SIN_OBLIGACIONES_FISCALES,
            "03020",
        )

        # Check if the result is a Customer instance
        assert isinstance(result, Customer)

    def test_get_all_customers(self):
        """Test case for getting all the customers"""
        result = self.customers.all()

        # Check if the result is a CustomerList instance
        assert isinstance(result, CustomerList)

        # Check if the total results count is correct
        assert len(result) == result.total_results

        # Check if all the items are Customer instances
        assert all(isinstance(customer, Customer) for customer in result)
