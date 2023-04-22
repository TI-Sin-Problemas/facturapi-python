"""FacturAPI object models"""
from collections.abc import Sequence
from datetime import datetime
from typing import Iterator, List, NamedTuple

from dateutil.parser import isoparse

from .constants import TaxSystem


class Address(NamedTuple):
    """Customer address"""

    zip: str
    country: str
    municipality: str = None
    state: str = None
    city: str = None
    street: str = None
    exterior: int = None
    interior: int = None
    neighborhood: str = None


class Customer(NamedTuple):
    """Customer object"""

    id: str
    created_at: datetime
    livemode: bool
    legal_name: str
    tax_id: str
    tax_system: TaxSystem
    address: Address
    email: str = None
    phone: int = None


class CustomerList(Sequence):
    """Customer list object"""

    def __init__(
        self, page: int, total_pages: int, total_results: int, data: List[Customer]
    ) -> None:
        self.page = page
        self.total_pages = total_pages
        self.total_results = total_results
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[Customer]:
        return self.data.__iter__()


def build_customer(api_response: dict) -> Customer:
    """Build a Customer object from an API response

    Args:
        api_response (dict): API response

    Returns:
        Customer: Customer object
    """
    return Customer(
        api_response.get("id"),
        isoparse(api_response.get("created_at")),
        api_response.get("livemode"),
        api_response.get("legal_name"),
        api_response.get("tax_id"),
        TaxSystem(api_response["tax_system"]),
        Address(**api_response["address"]),
        api_response.get("email"),
        api_response.get("phone"),
    )


def build_customer_list(api_response: dict) -> CustomerList:
    """Build a CustomerList from an API response

    Args:
        api_response (dict): API response

    Returns:
        CustomerList: List of customers
    """
    customers = [build_customer(item) for item in api_response["data"]]
    customer_list_kwargs = {
        "page": api_response.get("page"),
        "total_pages": api_response.get("total_pages"),
        "total_results": api_response.get("total_results"),
        "data": customers,
    }
    return CustomerList(**customer_list_kwargs)
