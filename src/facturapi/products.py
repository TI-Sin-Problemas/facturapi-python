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
        """Returns a paginated list of all products of an organization or search by parameters
        recieved

        Args:
            search (str, optional): String to search in product description or SKU.
            Defaults to None.
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

    def retrieve(self, product_id: str) -> dict:
        """Returns a single product object

        Args:
            product_def retrieve(self, product_id (str): Product ID

        Returns:
            dict: _description_
        """
        url = self._get_request_url([product_id])
        return self._execute_request("GET", url)

    def update(self, product_id: str, data: dict) -> dict:
        """Updates an existing product information

        Args:
            product_id (str): ID of the product to update
            data (dict): Product's new data to

        Returns:
            dict: Updated product object
        """
        url = self._get_request_url([product_id])
        return self._execute_request("PUT", url, json_data=data)
