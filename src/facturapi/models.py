"""FacturAPI object models"""
from collections.abc import Sequence
from typing import Iterator, List, NamedTuple


class Address(NamedTuple):
    """Address object"""

    zip: str
    municipality: str
    state: str
    city: str
    country: str
    street: str = None
    exterior: int = None
    interior: int = None
    neighborhood: str = None


class Customer(NamedTuple):
    """Customer object"""

    id: str
    created_at: str
    livemode: bool
    legal_name: str
    tax_id: str
    tax_system: str
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


def build_customer_list(api_response: dict) -> CustomerList:
    """Build a CustomerList from an API response

    Args:
        api_response (dict): API response

    Returns:
        CustomerList: List of customers
    """
    customers = []
    for item in api_response.get("data", []):
        customer_kwargs = {
            "id": item.get("id"),
            "created_at": item.get("created_at"),
            "livemode": item.get("livemode"),
            "legal_name": item.get("legal_name"),
            "tax_id": item.get("tax_id"),
            "tax_system": item.get("tax_system"),
            "email": item.get("email"),
            "phone": item.get("phone"),
        }
        address = Address(**item["address"])
        customers.append(Customer(**customer_kwargs, address=address))

    customer_list_kwargs = {
        "page": api_response.get("page"),
        "total_pages": api_response.get("total_pages"),
        "total_results": api_response.get("total_results"),
        "data": customers,
    }
    return CustomerList(**customer_list_kwargs)
