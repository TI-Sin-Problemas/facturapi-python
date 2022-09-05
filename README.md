![PyPI - Downloads](https://img.shields.io/pypi/dm/facturapi-python?logoColor=yellow&style=for-the-badge) ![PyPI](https://img.shields.io/pypi/v/facturapi-python?label=Latest&logo=pypi&logoColor=yellow&style=for-the-badge) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/facturapi-python?logo=python&logoColor=yellow&style=for-the-badge) ![GitHub Repo stars](https://img.shields.io/github/stars/TI-Sin-Problemas/facturapi-python?logo=github&style=for-the-badge) ![GitHub issues](https://img.shields.io/github/issues/TI-Sin-Problemas/facturapi-python?logo=github&style=for-the-badge)

# FacturAPI Unofficial Python client

This is an unofficial Python wrapper for [FacturAPI](https://facturapi.io/)

FacturAPI makes it easy for developers to generate valid Invoices in Mexico (known as Factura Electrónica or CFDI).

If you've ever used [Stripe](https://stripe.com/) or [Conekta](https://conekta.io/), you'll find FacturAPI very straightforward to understand and integrate in your server app.

## Install

```bash
pip install facturapi-python
```

## Getting started

### Create a customer

```python
from facturapi import Facturapi

api = facturapi("FACTURAPI_SECRET_KEY")

new_customer = api.customers.create({
  "legal_name": "Dunder Mifflin",
  "tax_id": "ABC101010111",
  "tax_system": "601",
  "email": "email@example.com",
  "phone": 6474010101,
  "address": {
    "street": "Blvd. Atardecer",
    "exterior": 142,
    "interior": 4,
    "neighborhood": "Centro",
    "city": "Huatabampo",
    "municipality": "Huatabampo",
    "zip": 86500,
    "state": "Sonora",
    "country": "MEX"
  }
})

```

### Create a product

```python
from facturapi import Facturapi

api = facturapi("FACTURAPI_SECRET_KEY")

new_product = api.products.create({
    "description": "Ukelele",
    "product_key": 60131324,
    "price": 345.6,
    "tax_included": true,
    "taxability": "01",
    "taxes": [{
        "type": "IVA",
        "rate": 0.16
        }],
    "local_taxes": [],
    "unit_key": "H87",
    "unit_name": "Elemento",
    "sku": "string"
})

```

### Create an invoice

```python
from facturapi import Facturapi

api = facturapi("FACTURAPI_SECRET_KEY")

new_invoice = api.invoices.create({
    "customer": "YOUR_CUSTOMER_ID", # You can also use a customer object instead
    "payment_form": api.catalogs.payment_forms.TRANSFERENCIA_ELECTRONICA,
    "items": [{
    "quantity": 1,
    "product": 'YOUR_PRODUCT_ID' # You can also use a product object instead
  }]
})

```

#### Download your invoice

```python
from facturapi import Facturapi

api = facturapi("FACTURAPI_SECRET_KEY")

with open("invoice.zip", "wb") as binary_file:
    invoice = api.invoices.download_zip("INVOICE_ID")
    binary_file.write(invoice)

```

#### Send your invoice by email

```python
from facturapi import Facturapi

api = facturapi("FACTURAPI_SECRET_KEY")

message = api.invoices.send_by_email("INVOICE_ID", "customer@email.com")

```

## Documentation

You can find more on what to do on the [official documentation](http://docs.facturapi.io.)

## Help

:warning: This is an unofficial project, the maintainers does not have any affiliation with FacturAPI or their developers. Any error with the service itself should be reported to the official support channels

### Found a bug?

If you find a bug for this API client, please create an issue on the [project's github page](https://github.com/TI-Sin-Problemas/facturapi-python/issues)

### Contribute

All PRs are welcome!
