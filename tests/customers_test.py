"""Customers endpoint tests"""
from datetime import datetime

from dateutil.relativedelta import relativedelta
from settings import API_KEY

from facturapi import Facturapi
from facturapi.constants import TaxSystem
from facturapi.models import Customer, CustomerList


class TestCustomers:
    """Test case for getting all the customers"""

    customers = Facturapi(API_KEY).customers
    customer_name = "PÚBLICO EN GENERAL"
    customer_tax_id = "XAXX010101000"

    def test_create_customer(self):
        """Test for customer creation"""
        tax_system = TaxSystem.SIN_OBLIGACIONES_FISCALES
        zip_code = "03020"
        result = self.customers.create(
            self.customer_name,
            self.customer_tax_id,
            tax_system,
            zip_code,
        )

        # Check if the result is a Customer instance
        assert isinstance(result, Customer)

        # Check if customer data is correct
        assertion_data = [
            result.legal_name == self.customer_name,
            result.tax_id == self.customer_tax_id,
            result.tax_system == tax_system,
            result.address.zip == zip_code,
        ]
        assert all(assertion_data)

    def test_get_all_customers(self):
        """Test case for getting all the customers"""
        result = self.customers.all()

        # Check if the result is a CustomerList instance
        assert isinstance(result, CustomerList)

        # Check if the total results count is correct
        assert len(result) == result.total_results

        # Check if all the items are Customer instances
        assert all(isinstance(customer, Customer) for customer in result)

    def test_search_customers(self):
        """Test customer search"""
        result = self.customers.all(search=self.customer_tax_id)

        # Check if “PÚBLICO EN GENERAL” is in the result
        assert self.customer_tax_id in [customer.tax_id for customer in result]

    def test_search_customers_by_date(self):
        """Test for customer search by date"""
        today = datetime.now()
        last_year = today - relativedelta(years=1)
        result = self.customers.all(start_date=last_year, end_date=today)

        # Check if all the customers in result where created in date range
        assert all(
            customer.created_at >= last_year and customer.created_at <= today
            for customer in result
        )

    def test_retrieve_one_customer(self):
        """Test to retrieve one customer from the API"""
        customers = self.customers.all()
        customer_id = customers[0].id
        result = self.customers.retrieve(customer_id)

        # Check if the retrieved customer is correct
        assert result.id == customer_id
