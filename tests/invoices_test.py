# """Invoices endpoint unit tests"""
from datetime import datetime
from src.facturapi.enums import CancelationReason, PaymentForm

from .mocks import MockCustomer, MockInvoice, MockProduct
from .testcase import FacturapiTestCase, assert_property_in, assert_status


class TestInvoicesEndpoint(FacturapiTestCase):
    """Invoices endpoint Test Cases"""

    mock_product = MockProduct()
    mock_customer = MockCustomer()
    endpoint = "invoices"

    def _generate_mock_invoice(self):
        """Returns mock items list"""
        customer = self.mock_customer._asdict()
        items = [{"product": self.mock_product._asdict()}]
        return MockInvoice(customer, items, PaymentForm.EFECTIVO.value)._asdict()

    def test_crd(self):
        """Test complete CRD"""

        # Create test
        endpoint = self._get_endpoint(self.endpoint)
        mock_invoice = self._generate_mock_invoice()
        new_invoice = endpoint.create(mock_invoice)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("id", new_invoice)

        invoice_id = new_invoice["id"]

        # Retrieve test
        retrieved_invoice = endpoint.retrieve(invoice_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("id", retrieved_invoice)

        # Cancelation test
        cancellation_reason = CancelationReason.ERRORS_WITHOUT_RELATION
        cancelled_invoice = endpoint.cancel(invoice_id, cancellation_reason)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("id", cancelled_invoice)

        # Get cancellation receipt
        cancellation_receipt = endpoint.get_cancellation_receipt(invoice_id)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert isinstance(cancellation_receipt, str)

    def test_get_all_invoices(self):
        """Get all invoices"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all()

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_search_invoices_by_product(self):
        """Search invoices by product description"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(search=self.mock_product.description)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_search_invoices_by_customer(self):
        """Search invoices by customer ID"""
        endpoint = self._get_endpoint(self.endpoint)
        customers_endpoint = self._get_endpoint("customers")
        customers = customers_endpoint.all()["data"]
        first_customer = customers[0]
        result = endpoint.all(customer_id=first_customer["id"])

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_get_invoices_created_last_year(self):
        """Get all invoices created last year"""
        endpoint = self._get_endpoint(self.endpoint)
        today = datetime.today()
        last_january = today.replace(year=today.year - 1, month=1, day=1)
        last_december = today.replace(year=today.year - 1, month=12, day=31)
        result = endpoint.all(start_date=last_january, end_date=last_december)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)

    def test_get_invoice_first_page(self):
        """Get first page of invoice limited by 5"""
        endpoint = self._get_endpoint(self.endpoint)
        result = endpoint.all(page=1, limit=5)

        assert_status(endpoint.last_status, endpoint.STATUS_OK)
        assert_property_in("data", result)
