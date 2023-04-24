"""Customers endpoint tests"""
from datetime import datetime
from random import randint

import pytest
from dateutil.relativedelta import relativedelta
from settings import API_KEY

from facturapi import Facturapi
from facturapi.constants import TaxSystem
from facturapi.models import Customer, CustomerList


class TestCustomers:
    """Test case for getting all the customers"""

    api = Facturapi(API_KEY)
    customer_name = "PÚBLICO EN GENERAL"
    customer_tax_id = "XAXX010101000"
    tax_system = TaxSystem.SIN_OBLIGACIONES_FISCALES
    zip_code = f"0300{randint(0, 9)}"
    customer = api.customers.create(
        customer_name,
        customer_tax_id,
        tax_system,
        zip_code,
    )

    def test_create_customer(self):
        """Test for customer creation"""

        # Check if the result is a Customer instance
        assert isinstance(self.customer, Customer)

        # Check if customer data is correct
        assertion_data = [
            self.customer.legal_name == self.customer_name,
            self.customer.tax_id == self.customer_tax_id,
            self.customer.tax_system == self.tax_system,
            self.customer.address.zip == self.zip_code,
        ]
        assert all(assertion_data)

    def test_get_all_customers(self):
        """Test case for getting all the customers"""
        result = self.api.customers.all()

        # Check if the result is a CustomerList instance
        assert isinstance(result, CustomerList)

        # Check if the total results count is correct
        assert len(result) == result.total_results

        # Check if all the items are Customer instances
        assert all(isinstance(customer, Customer) for customer in result)

    def test_search_customers(self):
        """Test customer search"""
        result = self.api.customers.all(search=self.customer_tax_id)

        # Check if “PÚBLICO EN GENERAL” is in the result
        assert self.customer_tax_id in [customer.tax_id for customer in result]

    def test_search_customers_by_date(self):
        """Test for customer search by date"""
        today = datetime.now()
        last_year = today - relativedelta(years=1)
        result = self.api.customers.all(start_date=last_year, end_date=today)

        # Check if all the customers in result where created in date range
        assert all(c.created_at >= last_year and c.created_at <= today for c in result)

    @pytest.mark.skipif(not customer, reason="Customer creaton failed")
    def test_retrieve_one_customer(self):
        """Test to retrieve one customer from the API"""
        result = self.api.customers.retrieve(self.customer.id)

        # Check if the retrieved customer is correct
        assert result.id == self.customer.id

    @pytest.mark.skipif(not customer, reason="Customer creaton failed")
    def test_update_client(self):
        """Test to update a specific client from the API"""
        email = "user@example.com"
        phone = "5512345678"
        zip_code = "01234"
        result = self.api.customers.update(
            self.customer.id, email=email, phone=phone, zip_code=zip_code
        )

        # Check if the result is correct
        assertions = [
            result.email == email,
            result.phone == phone,
            result.address.zip == zip_code,
        ]
        assert all(assertions)

    @pytest.mark.skipif(not customer, reason="Customer creaton failed")
    def test_delete_customer(self):
        """Test to delete a specific client from the API"""
        result = self.api.customers.delete(self.customer.id)

        # Check if the result is correct
        assert isinstance(result, Customer)
