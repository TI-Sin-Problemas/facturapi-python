"""Customer API endpoint"""
from datetime import datetime

from .http import BaseClient


class CustomersClient(BaseClient):
    """Customers API client"""

    endpoint = "customers"

    def create(self, data: dict):
        """Creates a new customer in your organization.

        Args:
            data (dict): Customer details

        Returns:
            dict: Created customer object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data)

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
        return self._execute_request("GET", url, params)

    def retrieve(self, customer_id: str) -> dict:
        """Retrieves a single customer object

        Args:
            customer_id (str): ID of the customer to retrieve

        Returns:
            dict: Customer object
        """
        url = self._get_request_url([customer_id])
        return self._execute_request("GET", url)

    def update(self, customer_id: str, data: dict) -> str:
        """Updates a customer object

        Args:
            customer_id (str): IF of the customer to update
            data (dict): Customer's new data

        Returns:
            str: Customer object
        """
        url = self._get_request_url([customer_id])
        return self._execute_request("PUT", url, json_data=data)
