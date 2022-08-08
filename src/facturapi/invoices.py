"""Invoices API endpoint"""
from .http import BaseClient


class InvoicesClient(BaseClient):
    """Products API client"""

    endpoint = "invoices"

    def create(self, data: dict) -> dict:
        """Creates a new invoice

        Args:
            data (dict): Invoice data

        Returns:
            dict: Created invoice object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data)
