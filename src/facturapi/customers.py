"""Customer API endpoint"""

from .http import BaseClient


class CustomersClient(BaseClient):
    """Customers API client"""

    endpoint = "customers"

    def create(self, data: dict):
        """Creates a new customer in your organization.

        Args:
            data (dict): Customer details

        Returns:
            dict: Created customer details
        """
        url = self._get_request_url()
        return self._execute_post_request(url, data)
