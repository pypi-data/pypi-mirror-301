import yaml
import os
import logging
from dnsconfigurator.dns_domain import DNSDomain
from dnsconfigurator.validate import validate_config

logger = logging.getLogger(__name__)

class DNSConfig:
    def __init__(self, filename):
        logger.info("Reading local DNS configuration")
        self.filename = filename
        self.config   = self.load_config()
        self.iplist   = self.config.get('iplist', {})
        self.default  = self.config.get('default', {})
        self.domains  = self.config.get('domains', {})
        self.fix_config_types()

    def list(self):
        return list(self.domains.keys())
    
    def load_config(self):
        """Load the YAML configuration file."""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Config file {self.filename} not found.")
        logger.debug(f"Loading config file '{self.filename}'")
        with open(self.filename, 'r') as file:
            config = yaml.safe_load(file)
        if not config:
            raise ValueError("Configuration file is empty or invalid.")
        return config

    # Convert dicts to list of dicts with name,value
    # And use default if field is non existing
    def fix_config_types(self):
        for field in ["a","cname","dkim","txt","mx"]:
            # Fix defaults
            if field not in self.default:
                self.default[field]=[]
            self.default[field] = self.fix_type(self.default[field])
            # Fix domains - insert default when missing
            for name,data in self.domains.items():
                if field not in data:
                    data[field] = self.default[field]
                else:
                    data[field] = self.fix_type(data[field])

    # Convert dict to list of dicts
    def fix_type(self,content):
        if isinstance(content, list):
            return content
        if isinstance(content, dict):
            return [{'name': k, 'value': v} for k, v in content.items()]
        if content == None:
            return []
        raise ValueError(f"Invalid variable {content}. Expected list, dict or None")

    def validate(self):
        validate_config(self.config)

    def domain(self, name):
        """Return the DNSDomain object for a specific domain."""
        logger.debug(f"Creating domain '{name}'")
        if not name:
            raise ValueError("No domain selected")
        if name not in self.domains:
            m = f"Domain {name} not found in the configuration."
            logger.error(m)
            raise ValueError(m)
        data = self.domains[name]
        # Create a new domain object
        domain = DNSDomain(name)
        # Get the main IP for the domain
        domain.ip=self.get_ip(data.get("ip"))
        #logger.debug(f"Looking up ip {data.get('ip')} -> {domain.ip}")

        # Add provider
        domain.provider = data["provider"] if "provider" in data else self.default.get("provider",None)

        # Add new records
        domain.add_a("@", domain.ip)
        for d in data["a"]:
            domain.add_a(d["name"], self.get_ip(d["value"]))
        for d in data["cname"]+data["dkim"]:
            domain.add_cname(d["name"], d["value"])
        for d in data["txt"]:
            domain.add_txt(d["name"], d["value"])
        for d in data["mx"]:
            domain.add_mx(d["priority"], d["value"])
        return domain

    def get_ip(self, ip):
        if ip in self.iplist:
            ip = self.iplist[ip]
        if not self.is_valid_ip(ip):
            raise ValueError(f"Invalid IP: {ip}")
        return ip

    def is_valid_ip(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not (0 <= int(part) <= 255):
                return False
        return True
