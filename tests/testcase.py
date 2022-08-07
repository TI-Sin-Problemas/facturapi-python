"""Facturapi Test Cases"""
from unittest import TestCase

from src.facturapi import Facturapi

from tests import settings


class FacturapiTestCase(TestCase):
    """Base Facturapi Test Case"""

    api = Facturapi(settings.FACTURAPI_KEY)
