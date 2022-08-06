"""HTTP Base Client"""
from abc import ABC, abstractmethod, property
import base64

from .exceptions import FacturapiException


class BaseClient(ABC):
    """BaseClient class to be extended by specific clients"""

    BASE_URL = "https://www.facturapi.io/"

    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_FOUND = 404

    @property
    @abstractmethod
    def endpoint(self) -> None:
        """All clients that inherit BaseClient should set endpoint to the base path for the API
        (e.g.: the customers API sets the value to 'customers')
        """

    def __init__(self, facturapi_key: str, api_version="v2") -> None:
        key_bytes = f"{facturapi_key}:".encode("ascii")
        b64_bytes = base64.b64encode(key_bytes)
        self.facturapi_key = b64_bytes.decode("ascii")
        self.api_version = api_version

    def __get_endpoint(self) -> str:
        """Returns specific endpoint set by API clients"""

        return self.endpoint

    def __get_api_version(self) -> str:
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

    def get_request_url(self, params: list = None, query: list = None) -> str:
        """Creates the URL to be used for the API request

        Args:
            params (list, optional): List of url params. Defaults to None.
            query (list, optional): List of query params. Defaults to None.

        Returns:
            str: URL for the API request
        """
        version = self.__get_api_version()
        param_string = "/".join(params) if params else ""
        quey_string = "&".join(query) if query else ""
        return f"{self.BASE_URL}{version}/{self.__get_endpoint()}/{param_string}?{quey_string}"
