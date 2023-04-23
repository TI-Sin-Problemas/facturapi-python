"""HTTP Base Client"""
from abc import ABC, abstractmethod
from requests import Session, Response

from .exceptions import FacturapiException


class BaseClient(ABC):
    """BaseClient class to be inherited by specific clients"""

    BASE_URL = "https://www.facturapi.io/"

    STATUS_OK = 200
    STATUS_CREATED = 201
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_AUTHENTICATED = 401
    STATUS_NOT_FOUND = 404
    STATUS_CONFLICT = 409
    STATUS_INTERNAL_SERVER_ERROR = 500

    @property
    @abstractmethod
    def endpoint(self) -> None:
        """All clients that inherit BaseClient should set endpoint to the base path for the API
        (e.g.: the customers API sets the value to 'customers')
        """

    def __init__(self, api_key: str, api_version="v2") -> None:
        self.api_key = api_key
        self.api_version = api_version
        self.last_status = None

        self.session = Session()
        self.session.auth = (self.api_key, "")
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
        return "{url}{api_version}/{endpoint}/{param_string}".format(
            url=self.BASE_URL,
            api_version=version,
            endpoint=self._get_endpoint(),
            param_string=param_string,
        )

    def _execute_request(
        self, method: str, url: str, query_params: dict = None, json_data: dict = None
    ) -> Response:
        """Executes a HTTP request

        Args:
            method (str): HTTP method. GET, POST, PUT or DELETE
            url (str): URL for the request
            query_params (dict, optional): Dictionary object of additional query. Defaults to None.
            json_data (dict, optional): For POST and PUT requests. Defaults to None.

        Returns:
            Response: API response
        """
        method_switch = {
            "GET": (self.session.get, {"params": query_params}),
            "POST": (self.session.post, {"json": json_data}),
            "PUT": (self.session.put, {"json": json_data}),
            "DELETE": (self.session.delete, {"params": query_params}),
        }

        request = method_switch.get(method.upper(), None)

        if not request:
            message = "Method {} not defined".format(method)
            raise FacturapiException(message)

        try:
            response = request[0](url, **request[1])
        except Exception as error:
            message = "Request error: {}".format(error)
            raise FacturapiException(message) from error

        self.last_status = response.status_code
        error_status_codes = [
            self.STATUS_BAD_REQUEST,
            self.STATUS_NOT_FOUND,
            self.STATUS_INTERNAL_SERVER_ERROR,
            self.STATUS_CONFLICT,
        ]

        if response.status_code in error_status_codes:
            json_response = response.json()
            raise FacturapiException(json_response["message"])

        if response.status_code == self.STATUS_NOT_AUTHENTICATED:
            raise FacturapiException("Wrong API KEY")

        return response

    def _get_download_file_url(self, file_format: str, object_id: str):
        return self._get_request_url([object_id, file_format])
