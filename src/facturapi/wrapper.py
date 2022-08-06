"""Facturapi API Client"""

from .customers import CustomersClient


class Facturapi:
    """Facturapi wrapper"""

    BASE_URL = "https://www.facturapi.io/"

    def __init__(self, facturapi_key: str) -> None:
        self.customers = CustomersClient(facturapi_key)
