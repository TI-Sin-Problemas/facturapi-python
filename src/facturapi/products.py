"""Products API endpoint"""
from .http import BaseClient


class ProductsClient(BaseClient):
    """Products API client"""

    endpoint = "products"

