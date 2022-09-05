"""Various utility endpoints"""
from .http import BaseClient


class HealthCheck(BaseClient):
    """Healthcheck service"""

    endpoint = "check"

    def check_status(self):
        """Checks service status

        Returns:
            bool: True if status is ok
        """
        url = self._get_request_url()
        print(url)

        response = self._execute_request("GET", url).json()

        print(response)
        return response["ok"]
