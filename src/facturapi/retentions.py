"""Retentions API endpoint"""
from .http import BaseClient


class RetentionsClient(BaseClient):
    """Retentions API client"""

    endpoint = "retentions"

    def create(self, data: dict) -> dict:
        """Creates a new Retention. If the receipt is created in a Live environment, it will be stamped and sent to satisfy

        Args:
            data (dict): Retention data

        Returns:
            dict: Created retention object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data).json()
