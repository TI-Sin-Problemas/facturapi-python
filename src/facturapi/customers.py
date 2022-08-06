"""Customer API endpoint"""
from datetime import datetime

from .http import BaseClient


class CustomersClient(BaseClient):
    """Customers API client"""

    endpoint = "customers"

    def __init__(self, facturapi_key: str, api_version="v2") -> None:
        super().__init__(facturapi_key, api_version)

    def create(self, data: dict):
        """Creates a new customer in your organization.

        Args:
            data (dict): Customer details

        Returns:
            dict: Created customer object
        """
        url = self._get_request_url()
        return self._execute_post_request(url, data)

    def all(
        self,
        search: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = None,
        limit: int = None,
    ) -> dict:
        """Retrieves a paginated list of customers from your organization

        Args:
            search (str, optional): Search by legal_name or tax_id. Defaults to None.
            start_date (datetime, optional): Limits the results by date. Defaults to None.
            end_date (datetime, optional): Limits the results by date. Defaults to None.
            page (int, optional): Page of the results list. Defaults to None.
            limit (int, optional): Maximum number of results. Defaults to None.

        Returns:
            dict: Response body
        """
        params = {}
        if search:
            params.update({"q": search})

        if start_date:
            params.update({"date[gt]": start_date.astimezone().isoformat()})

        if end_date:
            params.update({"date[lt]": end_date.astimezone().isoformat()})

        if page:
            params.update({"page": page})

        if limit:
            params.update({"limit": limit})

        url = self._get_request_url()
        return self._execute_get_request(url, params)

    def retrieve(self, customer_id: str) -> dict:
        """Retrieves a signle customer object

        Args:
            customer_id (str): ID of the customer to retrieve

        Returns:
            dict: Customer object
        """
        url = self._get_request_url([customer_id])
        return self._execute_get_request(url)
