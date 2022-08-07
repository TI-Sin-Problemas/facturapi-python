"""Products API endpoint"""
from .http import BaseClient


class ProductsClient(BaseClient):
    """Products API client"""

    endpoint = "products"

    def create(self, data: dict) -> dict:
        """Creates a new product or service in your catalog

        Args:
            data (dict): Product JSON data

        Returns:
            dict: Created product
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data)
