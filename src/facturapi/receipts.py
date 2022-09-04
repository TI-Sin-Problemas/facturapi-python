"""Receipts API endpoint"""
from .http import BaseClient


class ReceiptsClient(BaseClient):
    """Receipts API client"""

    endpoint = "receipts"
