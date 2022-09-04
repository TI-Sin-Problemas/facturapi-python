"""Organizations API endpoint"""
from .http import BaseClient


class OrganizationsClient(BaseClient):
    """Organizations API client"""

    endpoint = "organizations"

    def create(self, name: str) -> dict:
        """Creates a new Organization on the user account

        Args:
            name (str): Name of the new Organization

        Returns:
            dict: Created Organization object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data={"name": name}).json()
