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

    def all(self, search: str = None, page: int = None, limit: int = None) -> dict:
        """Returns a paginated list of all products of an organization or search by parameters recieved

        Args:
            search (str, optional): String to search in product description or SKU. Defaults to None.
            page (int, optional): Page of the result list. Defaults to None.
            limit (int, optional): Number of maximum quantity of results. Defaults to None.

        Returns:
            dict: Response data
        """
        params = {}
        if search:
            params.update({"q": search})
        if page:
            params.update({"page": page})

        if limit:
            params.update({"limit": limit})

        url = self._get_request_url()
        return self._execute_request("GET", url, params)
