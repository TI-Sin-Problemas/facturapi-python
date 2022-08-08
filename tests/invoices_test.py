"""Invoices endpoint unit tests"""
from src.facturapi.enums import PaymentForm

from tests.mocks import MockCustomer, MockInvoice, MockProduct
from tests.testcase import FacturapiTestCase


class TestInvoicesEndpoint(FacturapiTestCase):
    """Invoices endpoint Test Cases"""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.endpoint = self.api.invoices
        self.product = MockProduct()._asdict()
        customer_tax_id = MockCustomer().tax_id
        self.customer_id = self.api.customers.all(customer_tax_id)["data"][0]["id"]

    def test_create_invoice(self):
        """Create regular invoce"""
        invoice = MockInvoice(
            self.customer_id, [{"product": self.product}], PaymentForm.EFECTIVO.value
        )
        result = self.endpoint.create(invoice._asdict())
        status = self.endpoint.last_status

        self.assertIn("id", result)
        self.assertEqual(status, self.endpoint.STATUS_OK)
