"""Facturapi API Client"""

from .catalogs import CatalogsClient
from .customers import CustomersClient
from .enums import Catalogs
from .invoices import InvoicesClient
from .organizations import OrganizationsClient
from .products import ProductsClient
from .receipts import ReceiptsClient
from .retentions import RetentionsClient
from .tools import HealthCheck, ToolsClient


class Facturapi:  # pylint: disable=too-many-instance-attributes
    """Facturapi wrapper"""

    BASE_URL = "https://www.facturapi.io/"
    catalogs = Catalogs()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> str:
        healthcheck = self.healthcheck.check_status()
        if not healthcheck:
            return "Service down!"
        return "Service is ok"

    def __init__(self, facturapi_key: str) -> None:
        self.customers = CustomersClient(facturapi_key)
        self.products = ProductsClient(facturapi_key)
        self.invoices = InvoicesClient(facturapi_key)
        self.withholdings = RetentionsClient(facturapi_key)
        self.receipts = ReceiptsClient(facturapi_key)
        self.retentions = RetentionsClient(facturapi_key)
        self.organizations = OrganizationsClient(facturapi_key)
        self.healthcheck = HealthCheck(facturapi_key)
        self.tools = ToolsClient(facturapi_key)
        self.catalogs = CatalogsClient(facturapi_key)
