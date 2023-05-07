"""FacturAPI object models"""
from collections.abc import Sequence
from datetime import datetime
from typing import Iterator, List, NamedTuple

from dateutil.parser import isoparse

from .constants import IEPSMode, TaxFactor, Taxability, TaxSystem, TaxType

# The maximum number of items to display in a CustomerList.__repr__
REPR_OUTPUT_SIZE = 20


class BaseList(Sequence):
    """Base list class"""

    def __init__(
        self, page: int, total_pages: int, total_results: int, data: list
    ) -> None:
        self.page = page
        self.total_pages = total_pages
        self.total_results = total_results
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def __repr__(self) -> str:
        data = list(self[: REPR_OUTPUT_SIZE + 1])
        if len(data) > REPR_OUTPUT_SIZE:
            data[-1] = "...(remaining elements truncated)..."
        return f"<{self.__class__.__name__} {data}>"


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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.zip}>"


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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.legal_name}>"


class CustomerList(BaseList):
    """Customer list object"""

    def __init__(
        self, page: int, total_pages: int, total_results: int, data: List[Customer]
    ) -> None:
        super().__init__(page, total_pages, total_results, data)


class ValidationError(NamedTuple):
    """Message for the validation error"""

    path: str
    message: str

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.message}>"


class CustomerValidations:
    """Customer validation result"""

    def __init__(self, is_valid, errors) -> None:
        self.is_valid = is_valid
        self.errors = [ValidationError(e["path"], e["message"]) for e in errors]

    def __repr__(self) -> str:
        is_valid = "Valid" if self.is_valid else "Invalid"
        return f"<{self.__class__.__name__}: {is_valid} {self.errors}>"

    def __getitem__(self, item) -> ValidationError:
        return self.errors[item]

    def __len__(self) -> int:
        return len(self.errors)

    def __iter__(self) -> List[ValidationError]:
        return self.errors.__iter__()

    def get_messages(self) -> str:
        """Return a string with all the error messages

        Returns:
            str: Error messages
        """
        return "; ".join([e.message for e in self.errors])


class ProductTax(NamedTuple):
    """Tax object of a product"""

    rate: float
    type: TaxType = None
    factor: TaxFactor = None
    withholding: bool = False
    ieps_mode: IEPSMode = None


class Product(NamedTuple):
    """Product object"""

    id: str
    created_at: datetime
    livemode: bool
    description: str
    product_key: str
    price: float
    tax_included: bool
    taxes: List[ProductTax]
    local_taxes: List[ProductTax]
    unit_key: str
    unit_name: str
    sku: str
    taxability: Taxability = None


class ProductList(BaseList):
    """List of products"""

    def __init__(
        self, page: int, total_pages: int, total_results: int, data: List[Product]
    ) -> None:
        super().__init__(page, total_pages, total_results, data)


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


def build_product(api_response: dict) -> Product:
    """Build a Product object from an API response

    Args:
        api_response (dict): API response

    Returns:
        Product: Product object
    """

    taxability = api_response.get("taxability")
    taxes = api_response["taxes"]

    product_taxes = []
    for tax in taxes:
        tax_type = TaxType(tax["type"])
        factor = TaxFactor(tax["factor"])
        ieps_mode = IEPSMode(tax["ieps_mode"])
        product_taxes.append(
            ProductTax(tax["rate"], tax_type, factor, tax["withholding"], ieps_mode)
        )

    return Product(
        api_response.get("id"),
        isoparse(api_response.get("created_at")),
        api_response.get("livemode"),
        api_response.get("description"),
        api_response.get("product_key"),
        api_response.get("price"),
        api_response.get("tax_included"),
        product_taxes,
        api_response.get("local_taxes", []),
        api_response.get("unit_key"),
        api_response.get("unit_name"),
        api_response.get("sku"),
        Taxability(taxability) if taxability else None,
    )
