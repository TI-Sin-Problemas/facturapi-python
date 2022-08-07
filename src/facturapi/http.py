"""HTTP Base Client"""
from abc import ABC, abstractmethod
from requests import Session

from .exceptions import FacturapiException


class BaseClient(ABC):
    """BaseClient class to be inherited by specific clients"""

    BASE_URL = "https://www.facturapi.io/"

    STATUS_OK = 200
    STATUS_CREATED = 201
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_FOUND = 404

    @property
    @abstractmethod
    def endpoint(self) -> None:
        """All clients that inherit BaseClient should set endpoint to the base path for the API
        (e.g.: the customers API sets the value to 'customers')
        """

    def __init__(self, facturapi_key: str, api_version="v2") -> None:
        self.facturapi_key = facturapi_key
        self.api_version = api_version
        self.last_status = None

        self.session = Session()
        self.session.auth = (self.facturapi_key, "")
        self.session.headers.update({"Content-Type": "application/json"})

    def _get_endpoint(self) -> str:
        """Returns specific endpoint set by API clients"""

        return self.endpoint

    def _get_api_version(self) -> str:
        """Returns API version that is set in specific API clients.
        All clients that inherit BaseClient should set api_version to the version that the client
        is developed for (e.g.: the customers v1 client sets the value to 'v1')

        Raises:
            FacturapiException

        Returns:
            str: API version
        """
        if not self.api_version:
            raise FacturapiException("api_version must be defined")
        return self.api_version

    def _get_request_url(self, path_params: list = None) -> str:
        """Creates the URL to be used for the API request

        Args:
            path_params (list, optional): List of path parameters. Defaults to None.

        Returns:
            str: URL for the API request
        """
        version = self._get_api_version()
        param_string = "/".join(path_params) if path_params else ""
        return f"{self.BASE_URL}{version}/{self._get_endpoint()}/{param_string}"

    def _execute_get_request(self, url: str, params: dict = None) -> dict:
        """Executes a GET request to url

        Args:
            url (str): URL for the request
            params (dict, optional): Dictionary object of aditional query params . Defaults to None.

        Raises:
            FacturapiException

        Returns:
            dict: Respose body
        """
        try:
            response = self.session.get(url, params=params)
        except Exception as error:
            raise FacturapiException(f"Requests error: {error}") from error

        self.last_status = response.status_code

        return response.json()

    def _execute_post_request(self, url: str, data: dict) -> dict:
        """Executes a POST request to url

        Args:
            url (str): URL for the request
            data (dict): Data to send as body

        Raises:
            FacturapiException

        Returns:
            dict: Response body
        """
        try:
            response = self.session.post(url, json=data)
        except Exception as error:
            raise FacturapiException(f"Requests error: {error}") from error

        self.last_status = response.status_code

        return response.json()

    def _execute_put_request(self, url: str, data: dict) -> dict:
        """Executes a PUT request to url

        Args:
            url (str): URL for the request
            data (dict): Data to update

        Raises:
            FacturapiException

        Returns:
            dict: Updated object
        """
        try:
            response = self.session.put(url, json=data)
        except Exception as error:
            raise FacturapiException(f"Requests error: {error}") from error

        self.last_status = response.status_code

        return response.json()
