"""Facturapi API Client"""

from .customers import CustomersClient
from .products import ProductsClient
from .invoices import InvoicesClient
from .retentions import RetentionsClient


class Facturapi:
    """Facturapi wrapper"""

    BASE_URL = "https://www.facturapi.io/"

    def __init__(self, facturapi_key: str) -> None:
        self.customers = CustomersClient(facturapi_key)
        self.products = ProductsClient(facturapi_key)
        self.invoices = InvoicesClient(facturapi_key)
        self.withholdings = RetentionsClient(facturapi_key)
