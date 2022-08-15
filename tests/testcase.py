"""Facturapi Test Cases"""
from typing import Iterable
from src.facturapi import Facturapi

from tests import settings


class FacturapiTestCase:
    """Base Facturapi Test Case"""

    api = Facturapi(settings.FACTURAPI_KEY)

    def _get_endpoint(self, endpoint):
        return getattr(self.api, endpoint)


def assert_status(status: int, expected_status: int) -> None:
    """Asserts that status equals expected status"""
    assert status == expected_status, f"Status {status} returned"


def assert_property_in(prop: str, obj: Iterable) -> None:
    """Asserts that property is in object"""
    assert prop in obj, f"'{prop}' property not found in {obj}"
