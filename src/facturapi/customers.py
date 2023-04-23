"""Customer API endpoint"""
from datetime import datetime
from typing import Union

from .constants import TaxSystem
from .http import BaseClient
from .models import Customer, CustomerList, build_customer, build_customer_list


class CustomersClient(BaseClient):
    """Customers API client"""

    endpoint = "customers"

    def create(
        self,
        legal_name: str,
        tax_id: str,
        tax_system: Union[TaxSystem, str],
        zip_code: str,
        **kwargs
    ) -> Customer:
        """Creates a new customer in the organization .

        Args:
            legal_name (str): Company Name of the customer.
                Without the corporate regime (eg: S.A. de C.V)
            tax_id (str): RFC for customers in Mexico. Tax ID Number for foreigners
            tax_system (Union[TaxSystem, str]): Key of the customer's tax regime.
            zip_code (str): Address zip code.

        Kwargs:
            email (str, optional): Email address to which to send the generated invoices.
                Defaults to None.
            phone (str, optional): Phone number. Defaults to None.
            street (str, optional): Address street name. Defaults to None.
            exterior (str, optional): Address exterior number. Defaults to None.
            interior (str, optional): Address interior number. Defaults to None.
            neighborhood (str, optional): Address neighborhood. Defaults to None.
            city (str, optional): Address city. Defaults to None.
            municipality (str, optional): “Municipio” or "Delegación". Defaults to None.
            state (str, optional): If country is "MEX", name of the state. For foreigners,
                is the state code accodring to ISO 3166-2 standard. Defaults to None.
            country (str, optional): Country code according to ISO 3166-1 alpha-3 standard.
                Defaults to "MEX".

        Returns:
            Customer: Created customer
        """
        address_attrs = [
            "street",
            "exterior",
            "interior",
            "neighborhood",
            "city",
            "municipality",
            "state",
            "country",
        ]
        address = {
            "zip": zip_code,
            **{k: v for k, v in kwargs.items() if k in address_attrs},
        }

        if isinstance(tax_system, TaxSystem):
            tax_system = tax_system.value

        customer_attrs = ["email", "phone"]
        customer_data = {
            "legal_name": legal_name,
            "tax_id": tax_id,
            "tax_system": tax_system,
            "address": address,
            **{k: v for k, v in kwargs.items() if k in customer_attrs},
        }

        url = self._get_request_url()
        response = self._execute_request("POST", url, json_data=customer_data).json()
        return build_customer(response)

    # pylint: disable=too-many-arguments
    # All arguments are needed
    def all(
        self,
        search: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = None,
        limit: int = None,
    ) -> CustomerList:
        """Retrieves a paginated list of customers from your organization

        Args:
            search (str, optional): Search by legal_name or tax_id. Defaults to None.
            start_date (datetime, optional): Limits the results by date. Defaults to None.
            end_date (datetime, optional): Limits the results by date. Defaults to None.
            page (int, optional): Page of the results list. Defaults to None.
            limit (int, optional): Maximum number of results. Defaults to None.

        Returns:
            CustomerList: List-like object containing the customer search results
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
        response = self._execute_request("GET", url, params).json()

        return build_customer_list(response)

    def retrieve(self, customer_id: str) -> Customer:
        """Retrieves a single customer object

        Args:
            customer_id (str): ID of the customer to retrieve

        Returns:
            Customer: Retrieved customer
        """
        url = self._get_request_url([customer_id])
        response = self._execute_request("GET", url).json()
        return build_customer(response)

    def update(self, customer_id: str, **kwargs) -> Customer:
        """Updates an existing customer, assiging the values of the arguments sent.
        Arguments not sent in the request will not be modified.

        Args:
            customer_id (str): ID of the customer to update

        Kwargs:
            legal_name (str, optional): Company Name of the customer.
                Without the corporate regime (eg: S.A de C.V)
            tax_id (str, optional): RFC for customers in Mexico. Tax ID Number for foreigners
            tax_system (Union[TaxSystem, str]): Key of the customer's tax regime
            email (str, optional): Email address to which to send the generated invoices.
            phone (str, optional): Phone number.
            zip_code (str): Address zip code.
            street (str, optional): Address street name.
            exterior (str, optional): Address exterior number.
            interior (str, optional): Address interior number.
            neighborhood (str, optional): Address neighborhood.
            city (str, optional): Address city.
            municipality (str, optional): “Municipio” or "Delegación".
            state (str, optional): If country is "MEX", name of the state. For foreigners,
                is the state code accodring to ISO 3166-2 standard.
            country (str, optional): Country code according to ISO 3166-1 alpha-3 standard.

        Returns:
            Customer: Updated customer
        """
        customer_attrs = ["legal_name", "tax_id", "email", "phone"]
        data = {k: v for k, v in kwargs.items() if k in customer_attrs}

        tax_system = kwargs.get("tax_system")
        if tax_system:
            if isinstance(tax_system, TaxSystem):
                tax_system = tax_system.value
            data["tax_system"] = tax_system

        address_attrs = [
            "street",
            "exterior",
            "interior",
            "neighborhood",
            "city",
            "municipality",
            "state",
            "country",
        ]
        address = {k: v for k, v in kwargs.items() if k in address_attrs}

        zip_code = kwargs.get("zip_code")
        if zip_code:
            address["zip"] = zip_code

        if len(address) > 0:
            data["address"] = address

        url = self._get_request_url([customer_id])
        response = self._execute_request("PUT", url, json_data=data).json()
        return build_customer(response)

    def delete(self, customer_id: str) -> Customer:
        """Delete a customer from your organization

        Args:
            customer_id (str): ID of the customer to delete

        Returns:
            Customer: Deleted customer object
        """
        url = self._get_request_url([customer_id])
        response = self._execute_request("DELETE", url).json()
        return build_customer(response)

    def validate(self, customer_id: str) -> dict:
        """Validate customer's fiscal information

        Args:
            customer_id (str): ID of the customer to validate

        Returns:
            dict: JSON validation response
        """
        url = self._get_request_url([customer_id, "tax-info-validation"])
        return self._execute_request("GET", url).json()
