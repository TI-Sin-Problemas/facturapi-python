"""HTTP Base Client"""
import base64


class BaseClient:
    """BaseClient class to be extended by specific clients"""

    BASE_URL = "https://www.facturapi.io/"

    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400
    STATUS_NOT_FOUND = 404

    def __init__(self, facturapi_key: str, api_version="v2") -> None:
        key_bytes = f"{facturapi_key}:".encode("ascii")
        b64_bytes = base64.b64encode(key_bytes)
        self.facturapi_key = b64_bytes.decode("ascii")
        self.api_version = api_version
