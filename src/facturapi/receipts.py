"""Receipts API endpoint"""
from datetime import datetime
from .http import BaseClient


class ReceiptsClient(BaseClient):
    """Receipts API client"""

    endpoint = "receipts"

    def create(self, data: dict) -> dict:
        """Creates a new receipt. All receipts generate a self-invoicing URL that the customer can
        visit to fill in their tax information on a microsite with the branding of the organization

        Args:
            data (dict): Receipt data

        Returns:
            dict: Created receipt object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data).json()

    def all(
        self,
        search: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = None,
        limit: int = None,
    ) -> dict:
        """Returns a paginated list of all receipts in an organization
        or makes a search according to parameters

        Args:
            search (str, optional): Test to search in the description or the SKU of the items in
            the receipt. Defaults to None.
            start_date (datetime, optional): Lower limit of a date range. Defaults to None.
            end_date (datetime, optional): Upper limit of a date range. Defaults to None.
            page (int, optional): Result page to return, beginning with 1. Defaults to None.
            limit (int, optional): Number from 1 to 50 representing the maximum quantity of
            results to return. Used for pagination. Defaults to None.

        Returns:
            dict: List of receipts
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
        return self._execute_request("GET", url, params).json()

    def retrieve(self, receipt_id: str) -> dict:
        """Retrieves a single receipt object

        Args:
            receipt_id (str): ID of the receipt to retrieve

        Returns:
            dict: Receipt object
        """
        url = self._get_request_url([receipt_id])
        return self._execute_request("GET", url).json()
