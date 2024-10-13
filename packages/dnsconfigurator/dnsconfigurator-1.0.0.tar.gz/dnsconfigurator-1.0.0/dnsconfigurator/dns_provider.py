import logging
from abc import ABC, abstractmethod
import importlib
import requests
import json
import os
import code

logger = logging.getLogger(__name__)

class DNSProvider(ABC):
    """Abstract base class for DNS Providers."""

    def __init__(self, provider):
        self.provider = provider
        self.apikey   = self.get_key()
        self.zones    = {}
        self.domain   = None
        self.zoneid   = None
        self.records  = []
        self.setup()

    def set_domain(self, domain):
        if not self.zones:
            self.get_zones()
        try:
            zone = self.zones[domain]
        except:
            m=f"No zone for domain '{domain}' on remote '{self.provider}'"
            logger.error(m)
            raise ValueError(m)
        self.domain = zone["name"]
        self.zoneid = zone["id"]

    def get_key(self):
        envvar = f"API_{self.provider.upper()}"
        key = os.getenv(envvar)
        if not key:
            m = f"Cannot find {self.provider} API key in ENV variable '{envvar}'"
            logger.error(m)
            raise ValueError(m)
        return key

    def request(self, type, endpoint, data=None):
        if type not in ["get","post","delete","put","patch"]:
            raise ValueError("Unknown request method")
        url = f"{self.base}/{endpoint}"
        headers = self.headers
        logger.debug(f"Making {type} request to {url}")
        if data:
            logger.debug(f"Data: {data}")
        call = getattr(requests,type)
        response = call(url, headers=headers, data=json.dumps(data))
        if response.status_code == 404:
            raise requests.exceptions.RequestException(f"Error 404: No such resource '{endpoint}'")
        if not response.status_code == 200:
            code.interact(local = locals())
            raise requests.exceptions.RequestException(f"Unable to make request to endpoint '{endpoint}'")
        result = response.json()
        return result

    def req_get(self, endpoint):
        return self.request("get", endpoint)

    def req_post(self, endpoint, data):
        return self.request("post", endpoint, data)

    def req_delete(self, endpoint):
        return self.request("delete", endpoint)

    def req_put(self, endpoint, data):
        return self.request("put", endpoint, data)

    def req_patch(self, endpoints, data):
        return self.request("patch", endpoint, data)

    def unquote(selv, s):
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return s

    @abstractmethod
    def setup(self):
        """Setup base URL and headers."""
        pass

    @abstractmethod
    def get_zones(self):
        """Fetch zones from provider."""
        pass

    @abstractmethod
    def fetch(self, domain):
        """Fetch the DNS configuration from the remote provider."""
        pass

    @abstractmethod
    def update(self, record):
        """Update a record on the remote provider."""
        pass

    @abstractmethod
    def create(self, record):
        """Update a record on the remote provider."""
        pass

    @abstractmethod
    def delete(self, record):
        """Delete a record on the remote provider."""
        pass


class DNSProviderFactory:
    """Factory to create DNS provider instances based on the provider type."""

    @staticmethod
    def create_provider(provider_name):
        try:
            # Dynamically import the provider module
            module_name = f'dnsconfigurator.dns_provider_{provider_name.lower()}'
            module = importlib.import_module(module_name)
            logger.debug(f"Loading provider '{module_name}' module")


            # Dynamically get the provider class from the module
            class_name = f'DNSProvider{provider_name.capitalize()}'
            provider_class = getattr(module, class_name)

            # Instantiate the provider class with the given API key
            return provider_class(provider_name.capitalize())

        except (ModuleNotFoundError, AttributeError) as e:
            logger.error(f"Unsupported provider: '{provider_name}'")
            raise ValueError(f"Unsupported DNS provider: {provider_name}")
