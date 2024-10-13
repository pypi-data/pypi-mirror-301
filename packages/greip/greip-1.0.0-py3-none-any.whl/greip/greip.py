import requests

available_country_params = ['EN', 'AR', 'DE', 'FR', 'ES', 'JA', 'ZH', 'RU']
available_geoip_params = ['location', 'security', 'timezone', 'currency', 'device']

class CustomResponse:
    def __init__(self, **kwargs):
        #? Initialize attributes from the JSON response
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        #? Create a string representation of all attributes
        properties = {key: value for key, value in self.__dict__.items()}
        return f"CustomResponse({properties})"

    def __repr__(self):
        return self.__str__()

class Greip:
    """Greip instance: it's used to interact with the Greip API.

    Attributes:
        token (str): Your Greip API token.
        test_mode (bool): Whether to use the test mode or not.

    Raises:
        ValueError: If the token is not provided.

    Methods
    -------
        lookup(ip, params=None, lang="EN")
            Get geolocation information about an IP address.
        threats(ip)
            Get information about threats related to an IP address.
        bulk_lookup(ips, params=None, lang="EN")
            Get geolocation information about multiple IP addresses.
        country(country_code, params=None, lang="EN")
            Get information about a country.
        profanity(text, params=None, lang="EN")
            Check if a text contains profanity.
        asn(asn)
            Get information about an ASN.
        email(email)
            Validate an email address.
        phone(phone, country_code)
            Validate/lookup a phone number.
        iban(iban)
            Validate/lookup an IBAN number.
        payment(data)
            Check if a payment transaction is fraudulent.
    """

    def __init__(self, token: str, test_mode=False):
        #? Check if the token is provided
        if not token:
            raise ValueError("Token is required")
        self.token = token
        self.test_mode = test_mode

    def _make_http_request(self, endpoint: str, payload: dict):
        url = f"https://greipapi.com/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        #? Add the test mode to the payload if it's enabled
        if self.test_mode:
            payload['mode'] = 'test'
        
        response = requests.get(url, headers=headers, params=payload)

        #? Raise exception if the response status code is not 2xx
        if not response.ok:
            raise requests.exceptions.RequestException(response.text)

        json_response = response.json()
        if json_response.get('status') == 'error':
            raise requests.exceptions.RequestException(json_response['description'])

        data = json_response['data']
        return CustomResponse(**data)
    
    def _make_http_post_request(self, endpoint: str, payload: dict):
        url = f"https://greipapi.com/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        #? Add the test mode to the payload if it's enabled
        if self.test_mode:
            payload['mode'] = 'test'

        response = requests.post(url, headers=headers, json=payload)

        #? Raise exception if the response status code is not 2xx
        if not response.ok:
            raise requests.exceptions.RequestException(response.text)

        json_response = response.json()
        data = json_response['data']
        return CustomResponse(**data)

    def lookup(self, ip: str, params=None, lang="EN"):
        """Get geolocation information about an IP address.
        
        Parameters:
            ip (str): The IP address to lookup.
            params (list): The modules to include in the response.
            lang (str): The language of the response.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `ip` parameter is not provided.
            ValueError: If the `params` parameter is not a list.
            ValueError: If the `params` or `lang` are invalid.
        """

        if not ip:
            raise ValueError("You should pass the `ip` parameter.")
        
        if not isinstance(params, list):
            params = []
        
        #? Validate the params, and lang
        self._validate_params(params, available_geoip_params)
        self._validate_lang(lang)

        payload = {
            "ip": ip,
            "params": ",".join(params),
            "lang": lang.upper(),
        }

        return self._make_http_request("IPLookup", payload)

    def threats(self, ip: str):
        """Get information about threats related to an IP address.
        
        Parameters:
            ip (str): The IP address to lookup.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `ip` parameter is not provided.
        """
        if not ip:
            raise ValueError("You should pass the `ip` parameter.")
        
        payload = {
            "ip": ip,
        }

        return self._make_http_request("threats", payload)

    def bulk_lookup(self, ips: list, params=None, lang="EN"):
        """Get geolocation information about multiple IP addresses.

        Parameters:
            ips (list): The list of IP addresses to lookup.
            params (list): The modules to include in the response.
            lang (str): The language of the response.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `ips` parameter is not provided or not a list.
            ValueError: If the `params` parameter is not a list.
            ValueError: If the `params` or `lang` are invalid.
        """
        if not ips or not isinstance(ips, list) or len(ips) == 0:
            raise ValueError("You should pass the `ips` parameter as a list of IPs.")
        
        self._validate_ips(ips)
        if not isinstance(params, list):
            params = []
        
        #? Validate the params, and lang
        self._validate_params(params, available_geoip_params)
        self._validate_lang(lang)

        payload = {
            "ips": ",".join(ips),
            "params": ",".join(params),
            "lang": lang.upper(),
        }

        return self._make_http_request("BulkLookup", payload)

    def country(self, country_code: str, params=None, lang="EN"):
        """Get information about a country.

        Parameters:
            country_code (str): The ISO 3166-1 alpha-2 country code.
            params (list): The modules to include in the response.
            lang (str): The language of the response.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `country_code` parameter is not provided.
            ValueError: If the `country_code` is not in ISO 3166-1 alpha-2 format.
            ValueError: If the `params` parameter is not a list.
            ValueError: If the `params` or `lang` are invalid
        """

        if not country_code:
            raise ValueError("You should pass the `country_code` parameter.")
        if len(country_code) != 2:
            raise ValueError("The `country_code` parameter should be in ISO 3166-1 alpha-2 format.")
        
        if not isinstance(params, list):
            params = []
        
        #? Validate the params, and lang
        self._validate_params(params, available_country_params)
        self._validate_lang(lang)

        payload = {
            "CountryCode": country_code.upper(),
            "params": ",".join(params),
            "lang": lang.upper(),
        }

        return self._make_http_request("Country", payload)

    def profanity(self, text: str, params=None, lang="EN"):
        """Check if a text contains profanity.

        Parameters:
            text (str): The text to check.
            params (list): The modules to include in the response.
            lang (str): The language of the response.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `text` parameter is not provided.
            ValueError: If the `params` parameter is not a list.
            ValueError: If the `params` or `lang` are invalid.
        """

        if not text:
            raise ValueError("You should pass the `text` parameter.")
        
        if not isinstance(params, list):
            params = []
        
        #? Validate lang
        self._validate_lang(lang)

        payload = {
            "text": text,
            "params": ",".join(params),
            "lang": lang.upper(),
        }

        return self._make_http_request("badWords", payload)

    def asn(self, asn: str):
        """Get information about an ASN.

        Parameters:
            asn (str): The ASN to lookup.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `asn` parameter is not provided.
        """

        if not asn:
            raise ValueError("You should pass the `asn` parameter.")
        
        payload = {
            "asn": asn,
        }

        return self._make_http_request("ASNLookup", payload)

    def email(self, email: str):
        """Validate an email address.

        Parameters:
            email (str): The email address to validate.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `email` parameter is not provided.
        """

        if not email:
            raise ValueError("You should pass the `email` parameter.")
        
        payload = {
            "email": email,
        }

        return self._make_http_request("validateEmail", payload)
    
    def phone(self, phone: str, country_code: str):
        """Validate/lookup a phone number.

        Parameters:
            phone (str): The phone number to validate.
            country_code (str): The ISO 3166-1 alpha-2 country code.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `phone` or `country_code` parameters are not provided.
            ValueError: If the `country_code` is not in ISO 3166-1 alpha-2 format.
        """

        if not phone:
            raise ValueError("You should pass the `phone` parameter.")
        
        if len(country_code) != 2:
            raise ValueError("The `country_code` parameter should be in ISO 3166-1 alpha-2 format.")
        
        payload = {
            "phone": phone,
            "countryCode": country_code,
        }

        return self._make_http_request("validatePhone", payload)

    def iban(self, iban: str):
        """Validate/lookup an IBAN number.

        Parameters:
            iban (str): The IBAN number to validate.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `iban` parameter is not provided.
        """

        if not iban:
            raise ValueError("You should pass the `iban` parameter.")
        
        payload = {
            "iban": iban,
        }

        return self._make_http_request("validateIBAN", payload)

    def payment(self, data: dict):
        """Check if a payment transaction is fraudulent.

        Parameters:
            data (dict): The payment data to check.

        Returns:
            CustomResponse: The response object.

        Raises:
            ValueError: If the `data` parameter is not provided or not a dictionary.
        """

        if not data or not isinstance(data, dict):
            raise ValueError("You should pass the `data` parameter as a dictionary.")
        
        payload = {
            "data": data,
        }

        return self._make_http_post_request("paymentFraud", payload)

    #? Helper methods for validation
    def _validate_params(self, params, valid_params):
        for param in params:
            if param not in valid_params:
                raise ValueError(f'The "{param}" module is unknown. Check available params in the documentation.')

    def _validate_lang(self, lang):
        available_languages = ["EN", "AR", "DE", "FR", "ES", "JA", "ZH", "RU"]
        if lang.upper() not in available_languages:
            raise ValueError(f'The language "{lang}" is invalid. Use one of: {available_languages}')

    def _validate_ips(self, ips):
        for ip in ips:
            if len(ip) < 7:
                raise ValueError("Invalid IP address in the `ips` list.")
