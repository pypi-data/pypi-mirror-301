# SAP

This module provides an interface to interact with the SAP server. It includes methods to get quote details and list quotes from a given sales organization.

---

## Installation

To install the SAP module, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## Usage

### Initialization

To initialize the SAP class, you need to provide a username and password for authentication.
Optionally, you can provide the URL of the SAP server.

```python
from bits_aviso_python_sdk.services.sap import SAP

sap = SAP(username='your_username', password='your_password', url='http://sap.broadinstitute.org:8085')
```

### Examples

---

#### Get Quote Details

To get the details of a specific quote, use the `get_quote_details` method:

```python
quote_number = '12345'
quote_details, error = sap.get_quote_details(quote_number)

if error:
    print(f"Error: {error}")
else:
    print(f"Quote Details: {quote_details}")
```

---

#### List All Quotes

To list all quotes from a given sales organization, use the `list_all_quotes` method:

```python
sales_org = '1000'
quotes, error = sap.list_all_quotes(sales_org)

if error:
  print(f"Error: {error}")
else:
  print(f"Quotes: {quotes}")
```

---

## Functions

The SAP module provides the following functions:

---

### `__init__(username, password, url)`
- **Args:**
  - `username` (str): The username for authentication.
  - `password` (str): The password for authentication.
  - `url` (str): The URL of the SAP server.

---

### `api_handler(payload)`
- **Args:**
  - `payload` (dict): The payload to send to the SAP server.
- **Returns:**
- `dict, dict`: The response data and the error payload.

---

### `get_quote_details(quote_number)`

- **Args:**
  - `quote_number` (str): The quote number to get details for.
- **Returns:**
  - `dict, dict`: The quote data and the error payload.

---

### `list_all_quotes(sales_org)`

- **Args:**
  - `sales_org` (str): The sales organization to list quotes for.
- **Returns:**
  - `list[dict], dict`: The quote data and the error payload.

---

## Error Handling

If an error occurs during the execution of a method,
the method will return a tuple containing `None` for the data and an error payload.

```json
{
    "Error": "An error message will be here",
    "Function": "The function that caused the error"
}
```
---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
