"""Facturapi API Client"""

from .customers import CustomersClient
from .enums import Catalogs
from .invoices import InvoicesClient
from .products import ProductsClient
from .receipts import ReceiptsClient
from .retentions import RetentionsClient
from .organizations import OrganizationsClient


class Facturapi:
    """Facturapi wrapper"""

    BASE_URL = "https://www.facturapi.io/"
    catalogs = Catalogs()

    def __init__(self, facturapi_key: str) -> None:
        self.customers = CustomersClient(facturapi_key)
        self.products = ProductsClient(facturapi_key)
        self.invoices = InvoicesClient(facturapi_key)
        self.withholdings = RetentionsClient(facturapi_key)
        self.receipts = ReceiptsClient(facturapi_key)
        self.retentions = RetentionsClient(facturapi_key)
        self.organizations = OrganizationsClient(facturapi_key)
