"""Products API endpoint"""
from typing import List, Union

from .constants import Taxability
from .http import BaseClient
from .models import Product, ProductList, build_product, build_product_list


class ProductsClient(BaseClient):
    """Products API client"""

    endpoint = "products"

    def create(  # pylint: disable=too-many-arguments
        self,
        description: str,
        product_key: str,
        price: Union[int, float],
        tax_included: bool = True,
        taxes: List[dict] = None,
        unit_key: str = "H87",
        **kwargs,
    ) -> Product:
        """Creates a new product or service in your Facturapi catalog

        Args:
            description (str): Description of the good or service as it will appear on the
                invoice.\n
            product_key (str): Product/service key, from the SAT catalog.\n
            price (Union[int, float]): Price per unit of the good or service.\n
            tax_included (bool, optional): True if all applicable taxes are included in the price.
                False if price does not include taxes. Defaults to True.\n
            taxes (List[dict], optional): List of taxes to apply to the product.
                If None, default taxes will apply. If empty list (`[]`) product is tax exempt.
                Default:
                ```
                [{
                    "rate": 0.16,
                    "type": "IVA",
                    "factor": "Tasa",
                    "withholding": False
                }]
                ```\n
            unit_key (str, optional): Unit of measure key, from the SAT catalog. Defaults to "H87".
            **kwargs:
                taxability (Union[Taxability, str], optional): Represents whether the good or
                    service is subject to tax or not. Defaults to None.\n
                unit_name (str, optional): Word that represents the unit of measurement of you
                    product. Must be related to the unit key unit_key. Defaults to None.\n
                sku (str, optional): Identifier for internal use designated by the company.
                    Defaults to None.\n

        Returns:
            Product: Created product
        """
        data = {
            "description": description,
            "product_key": product_key,
            "price": price,
            "tax_included": tax_included,
            "unit_key": unit_key,
            **{k: v for k, v in kwargs.items() if k in ["unit_name", "sku"]},
        }

        if taxes is not None:
            data.update({"taxes": taxes})

        taxability = kwargs.get("taxability")
        if isinstance(taxability, Taxability):
            taxability = taxability.value
        if taxability:
            data.update({"taxability": taxability})

        url = self._get_request_url()
        response = self._execute_request("POST", url, json_data=data).json()
        return build_product(response)

    def all(
        self, search: str = None, page: int = None, limit: int = None
    ) -> ProductList:
        """Returns a paginated list of all products of an organization or search by parameters
        recieved

        Args:
            search (str, optional): String to search in product description or SKU.
            Defaults to None.
            page (int, optional): Page of the result list. Defaults to None.
            limit (int, optional): Number of maximum quantity of results. Defaults to None.

        Returns:
            ProductList: List-like object containing the product search results
        """
        kwargs = {"q": search, "page": page, "limit": limit}
        params = {k: v for k, v in kwargs.items() if v}
        url = self._get_request_url()
        response = self._execute_request("GET", url, params).json()
        return build_product_list(response)

    def retrieve(self, product_id: str) -> Product:
        """Returns a single product object

        Args:
            product_id (str): Product ID

        Returns:
            Product: Retrieved product
        """
        url = self._get_request_url([product_id])
        response = self._execute_request("GET", url).json()
        return build_product(response)

    def update(self, product_id: str, **kwargs) -> Product:
        """Updates an existing product

        Updates the information of an existing product.
        Arguments not declared will not be modified.

        Args:
            product_id (str): ID of the product to update.
            **kwargs: Keyword arguments containing product data to update.
                description: Description of the good or service as it will appear on the invoice.
                product_key: Product/service key, from the SAT catalog.
                price: Price per unit of the good or service.
                tax_included: True if taxes are included in the price, False otherwise.
                taxability: Code representing whether the good or service is subject to tax or not.
                taxes: List of taxes to apply to the product.
                    If empty list (`[]`) product is tax exempt.
                    Example:
                    ```
                    [{
                        "rate": 0.16,
                        "type": "IVA",
                        "factor": "Tasa",
                        "withholding": False
                    }]
                    ```
                unit_key: Unit of measure key, from the SAT catalog
                unit_name: Word that represents the unit of measurement of your product.
                    Must be related to `unit_key`.
                sku: Identifier for internal use designated by the company.

        Returns:
            Product: Updated product object
        """
        allowed_args = [
            "description",
            "product_key",
            "price",
            "tax_included",
            "unit_key",
            "sku",
        ]
        data = {k: v for k, v in kwargs.items() if k in allowed_args}

        taxes = kwargs.get("taxes")
        if taxes is not None:
            data.update({"taxes": taxes})

        taxability = kwargs.get("taxability")
        if isinstance(taxability, Taxability):
            taxability = taxability.value
        if taxability:
            data.update({"taxability": taxability})

        url = self._get_request_url([product_id])
        response = self._execute_request("PUT", url, json_data=data).json()
        return build_product(response)

    def delete(self, product_id: str) -> Product:
        """Deletes the product from your organization

        Args:
            product_id (str): ID of the product to delete

        Returns:
            Product: Deleted product object
        """
        url = self._get_request_url([product_id])
        response = self._execute_request("DELETE", url).json()
        return build_product(response)
