"""Receipts API endpoint"""
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
