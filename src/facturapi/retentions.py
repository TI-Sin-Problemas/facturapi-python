"""Retentions API endpoint"""
from .http import BaseClient


class RetentionsClient(BaseClient):
    """Retentions API client"""

    endpoint = "retentions"
