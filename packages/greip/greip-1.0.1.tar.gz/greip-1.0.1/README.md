# Greip Python SDK

The Greip Python SDK allows you to easily interact with the Greip API for various functionalities, including IP geolocation, threat intelligence, email validation, and more.

[Report Issue](https://github.com/Greipio/python/issues/new) ·
[Request Feature](https://github.com/Greipio/python/discussions/new?category=ideas)
· [Greip Website](https://greip.io/) · [Documentation](https://docs.greip.io/)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Greipio/python?color=green&label=Minified%20size&logo=github)
&nbsp;&nbsp;
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/apache-2-0)
&nbsp;&nbsp;
![API Status](https://img.shields.io/website?down_color=orange&down_message=down&label=API%20status&up_color=green&up_message=up&url=https%3A%2F%2Fgreipapi.com)

---

## Installation

You can install the Greip SDK via pip. Run the following command:

```bash
pip install greip
```

## Usage

To use the Greip SDK, you need to initialize a Greip object with your API token. Here’s a basic example:

```python
import greip

# Initialize the Greip instance with your API token
greip_instance = greip.Greip("YOUR_API_TOKEN")

# Example: Lookup IP information
response = greip_instance.lookup("1.1.1.1")
print(response)  # Access properties like response.ip, response.country, etc.
```

## Methods

The Greip SDK provides various methods to interact with the API:

- **lookup(ip, params=None, lang=“EN”)**: Get geolocation information about an IP address.
- **threats(ip)**: Get information about threats related to an IP address.
- **bulk_lookup(ips, params=None, lang=“EN”)**: Get geolocation information about multiple IP addresses.
- **country(country_code, params=None, lang=“EN”)**: Get information about a country.
- **profanity(text, params=None, lang=“EN”)**: Check if a text contains profanity.
- **asn(asn)**: Get information about an ASN.
- **email(email)**: Validate an email address.
- **phone(phone,** country_code): Validate/lookup a phone number.
- **iban(iban)**: Validate/lookup an IBAN number.
- **payment(data)**: Check if a payment transaction is fraudulent.

## Example of Method Usage

```python
# Lookup country information
country_info = greip_instance.country("US")
print(country_info)  # Access properties like country_info.countryName, country_info.population, etc.
```

## Development mode

If you need to test the integration without affecting your account subscription usage you can simple set the `test_mode` attribute to `True` when you initialize the Greip instance, here's an example:

```python
greip_instance = greip.Greip("YOUR_API_TOKEN", test_mode=True)
```

> [!WARNING]
> Enabling the development environment will lead to return fake information. Just make sure to not use it in production.

## Error Handling

The SDK raises ValueError for invalid input parameters and requests.exceptions.RequestException for issues related to API requests. Ensure you handle exceptions properly in your code.

```python
try:
    response = greip_instance.lookup("INVALID_IP")
except ValueError as ve:
    print(f"ValueError: {ve}")
except requests.exceptions.RequestException as re:
    print(f"RequestException: {re}")
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bugs you encounter.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
