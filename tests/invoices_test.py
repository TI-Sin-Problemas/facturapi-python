"""Invoices endpoint unit tests"""
from datetime import datetime
from src.facturapi.enums import PaymentForm

from tests.mocks import MockCustomer, MockInvoice, MockProduct
from tests.testcase import FacturapiTestCase


class TestInvoicesEndpoint(FacturapiTestCase):
    """Invoices endpoint Test Cases"""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.invoices
        self.product = MockProduct()
        customer_tax_id = MockCustomer().tax_id
        self.customer_id = self.api.customers.all(customer_tax_id)["data"][0]["id"]

    def _get_invoice_id(self):
        """Returns mock invoice ID"""
        return self.endpoint.all(search=self.product.description)["data"][0]["id"]

    def test_create_invoice(self):
        """Create regular invoce"""
        items = [{"product": self.product._asdict()}]
        invoice = MockInvoice(self.customer_id, items, PaymentForm.EFECTIVO.value)
        result = self.endpoint.create(invoice._asdict())
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_all_invoices(self):
        """Get all invoices"""
        result = self.endpoint.all()
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_search_invoices_by_product(self):
        """Search invoices by product description"""
        result = self.endpoint.all(search=self.product.description)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_search_invoices_by_customer(self):
        """Search invoices by customer ID"""
        result = self.endpoint.all(customer_id=self.customer_id)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_invoices_created_last_year(self):
        """Get all invoices created last year"""
        today = datetime.today()
        last_january = today.replace(year=today.year - 1, month=1, day=1)
        last_december = today.replace(year=today.year - 1, month=12, day=31)
        result = self.endpoint.all(start_date=last_january, end_date=last_december)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_get_invoice_first_page(self):
        """Get first page of invoice limited by 5"""
        result = self.endpoint.all(page=1, limit=5)
        status = self.endpoint.last_status

        self.assertIn("data", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)

    def test_retrieve_invoice_object(self):
        """Retrieve single invoice"""
        invoice_id = self._get_invoice_id()
        result = self.endpoint.retrieve(invoice_id)
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)
