"""Catalogs API endpoint"""
from .http import BaseClient


class CatalogsClient(BaseClient):
    """Catalogs API client"""

    endpoint = "catalogs"

    def search_products(self, search: str, page: int = None, limit: int = None) -> dict:
        """Search in SAT's Products/Services catalog, which contains the key to include in the
        invoice

        Args:
            search (str): Text to search on the description of the category.
            page (int, optional): Page of results to return, beginning from page 1.
            Defaults to None.
            limit (int, optional): Number from 1 to 100, represents the maximum quiantity of
            results to return. Defaults to None.

        Returns:
            dict: List of products or services matching the query
        """
        params = {"q": search}

        if page:
            params.update({"page": page})
        if limit:
            params.update({"limit": limit})

        url = self._get_request_url(["products"])
        return self._execute_request("GET", url, params).json()

    def search_units_of_measurement(
        self, search: str, page: int = None, limit: int = None
    ) -> dict:
        """Search in SAT's Units of Measurement catalog

        Args:
            search (str): Test to search in the description of the unit of measurement
            page (int, optional): Page of results to return, beginning from page 1.
            Defaults to None.
            limit (int, optional): Number from 1 to 100, represents the maximum quiantity of
            results to return. Defaults to None.

        Returns:
            dict: List of units of measurement
        """
        params = {"q": search}

        if page:
            params.update({"page": page})
        if limit:
            params.update({"limit": limit})

        url = self._get_request_url(["units"])
        return self._execute_request("GET", url, params).json()
