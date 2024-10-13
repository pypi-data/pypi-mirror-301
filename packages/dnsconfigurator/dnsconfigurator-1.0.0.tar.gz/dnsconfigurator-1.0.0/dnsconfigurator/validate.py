import yaml
import re
from cerberus import Validator

# Custom validators
def is_ip_address(field, value, error):
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if not ip_pattern.match(value):
        error(field, "must be a valid IP address")

def is_fqdn(field, value, error):
    fqdn_pattern = re.compile(
        r'^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    )
    if not fqdn_pattern.match(value):
        error(field, "must be a valid fully qualified domain name (FQDN)")

def is_valid_identifier(field, value, error, allowed_values):
    if value not in allowed_values:
        error(field, f"must be a valid identifier from the iplist ({', '.join(allowed_values)})")

def validate_ip_presence(document, config):
    # Ensure each domain has an 'ip' either directly or from the 'default' section
    default_ip = config.get('default', {}).get('ip')
    for domain, settings in document.get('domains', {}).items():
        if not settings.get('ip') and not default_ip:
            raise ValueError(f"Domain '{domain}' is missing an 'ip' entry and no default 'ip' is provided.")

# Define the Cerberus schema
def get_schema(config):
    return {
        'iplist': {
            'type': 'dict',
            'keysrules': {'type': 'string'},
            'valuesrules': {'type': 'string', 'check_with': is_ip_address},
            'required': True
        },
        'default': {
            'type': 'dict',
            'schema': {
                'ip': {'type': 'string', 'nullable': True},
                'mx': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'priority': {'type': 'integer', 'required': True},
                            'value': {'type': 'string', 'check_with': is_fqdn, 'required': True}
                        }
                    }
                },
                'txt': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {'type': 'string', 'nullable': True},
                            'value': {'type': 'string', 'required': True}
                        }
                    }
                },
                'cname': {
                    'type': 'dict',
                    'keysrules': {'type': 'string'},
                    'valuesrules': {'type': 'string', 'nullable': True}
                },
                'dkim': {
                    'type': 'dict',
                    'keysrules': {'type': 'string'},
                    'valuesrules': {'type': 'string', 'required': True}
                }
            }
        },
        'domains': {
            'type': 'dict',
            'keysrules': {'type': 'string', 'check_with': is_fqdn},
            'valuesrules': {
                'type': 'dict',
                'schema': {
                    'ip': {
                        'type': 'string',
                        'check_with': lambda field, value, error: is_valid_identifier(field, value, error, config.get('iplist', {}).keys()),
                        'required': False
                    },
                    'mx': {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'priority': {'type': 'integer', 'required': True},
                                'value': {'type': 'string', 'check_with': is_fqdn, 'required': True}
                            }
                        },
                        'required': False
                    },
                    'txt': {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'name': {'type': 'string', 'nullable': True},
                                'value': {'type': 'string', 'required': True}
                            }
                        },
                        'required': False
                    },
                    'a': {
                        'type': 'dict',
                        'keysrules': {'type': 'string'},
                        'valuesrules': {
                            'type': 'string',
                            'check_with': lambda field, value, error: is_valid_identifier(field, value, error, config.get('iplist', {}).keys())
                        },
                        'required': False
                    },
                    'cname': {
                        'type': 'dict',
                        'keysrules': {'type': 'string'},
                        'valuesrules': {'type': 'string', 'nullable': True},
                        'required': False
                    },
                    'dkim': {
                        'type': 'dict',
                        'keysrules': {'type': 'string'},
                        'valuesrules': {'type': 'string', 'required': True},
                        'required': False
                    }
                }
            }
        }
    }

def validate_config(config):
    v = Validator(get_schema(config))
    if not v.validate(config):
        raise ValueError(f"Config validation failed: {v.errors}")
    
    # Custom validation for IP presence in domains
    validate_ip_presence(config, config)
    
    return True

