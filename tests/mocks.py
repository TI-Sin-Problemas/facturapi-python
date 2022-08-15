"""Mock classes for testing"""
from typing import NamedTuple


class MockAddress(NamedTuple):
    """Mock address generator"""

    zip: str = "01000"


class MockCustomer(NamedTuple):
    """Mock customer generator"""

    legal_name: str = "Publico General"
    tax_id: str = "XAXX010101000"
    tax_system: str = "601"
    address: dict = MockAddress()._asdict()


class MockProduct(NamedTuple):
    """Mock product class"""

    description: str = "Ukulele"
    product_key: str = "60131324"
    price: float = 345.6


class MockInvoice(NamedTuple):
    """Mock invoice class"""

    customer: dict
    items: list
    payment_form: str
