"""Organizations API endpoint"""
from datetime import datetime
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

    def all(
        self,
        search: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = None,
        limit: int = None,
    ) -> dict:
        """Returns a paginated list of all the organizations registered under your account
        or makes a search according to parameters

        Args:
            search (str, optional): Text to search on commercial name, legal name or tax ID. Defaults to None.
            start_date (datetime, optional): Lower limit of a date range. Defaults to None.
            end_date (datetime, optional): Upper limit of a date range. Defaults to None.
            page (int, optional): Result page to return, beginning with 1. Defaults to None.
            limit (int, optional): Number from 1 to 50 representing the maximum quantity of
            results to return. Used for pagination. Defaults to None.

        Returns:
            dict: List of organizations
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

    def update(self, organization_id: str, data: dict) -> dict:
        """Updates the fiscal data of the organization

        Args:
            organization_id (str): ID of the organization
            data (dict): Organization data to update

        Returns:
            dict: Updated organization object
        """
        url = self._get_request_url([organization_id, "legal"])
        return self._execute_request("PUT", url, json_data=data).json()

    def upload_csd(
        self, organization_id: str, cer_file: bytes, key_file: bytes, password: str
    ) -> dict:
        """Uploads the files of the Digital Seal Certificate (CSD) provided by SAT.
        This call should also be used to replace existing certificates should new ones be requested

        Args:
            organization_id (str): ID of the organization
            cer_file (bytes): Binary content of the .cer file
            key_file (bytes): Binary content of the .key file
            password (str): Certificate key password

        Returns:
            dict: Updated organization object
        """

        data = {"cerFile": cer_file, "keyFile": key_file, "password": password}
        url = self._get_request_url([organization_id, "certificate"])
        return self._execute_request("PUT", url, json_data=data)

    def upload_logo(self, organization_id: str, file: bytes) -> dict:
        """Uploads the organization's logo thet will be used for the PDF invoices and emails sent
        to the customer

        Args:
            organization_id (str): ID of the organization
            file (bytes): Logo file to be uploaded

        Returns:
            dict: Organization object
        """
        url = self._get_request_url([organization_id, "logo"])
        return self._execute_request("PUT", url, json_data={"file": file})
