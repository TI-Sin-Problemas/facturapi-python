"""Organizations API endpoint"""
from .http import BaseClient


class OrganizationsClient(BaseClient):
    """Organizations API client"""

    endpoint = "organizations"
