"""Various utility endpoints"""
from .http import BaseClient


class HealthCheck(BaseClient):
    """Healthcheck service"""

    endpoint = "check"

    def check_status(self) -> bool:
        """Checks service status

        Returns:
            bool: True if status is ok
        """
        url = self._get_request_url()
        return self._execute_request("GET", url).json()["ok"]


class ToolsClient(BaseClient):
    """Tools API endpoint"""

    endpoint = "tools"

    def validate_tax_id(self, tax_id: str) -> dict:
        """Check the status of a tax ID (RFC) in the list of EFOS (Companies that Invoice
        Simulated Operations). By appearing on this list, the RFC is or was suspected of engaging
        in simulation of fiscal operations.

        Args:
            tax_id (str): Tax ID (RFC)

        Returns:
            dict: The is_valid Boolean property is included, which Facturapi resolves by
            interpreting the response. A value of true for this property indicates that the RFC has
            no unresolved issues and is problem-free; and the opposite for false. Additionally, you
            can consult the data property to see the raw values of the SAT query.
        """
        url = self._get_request_url()
        return self._execute_request("GET", url, {"tax_id": tax_id}).json()["efos"]
