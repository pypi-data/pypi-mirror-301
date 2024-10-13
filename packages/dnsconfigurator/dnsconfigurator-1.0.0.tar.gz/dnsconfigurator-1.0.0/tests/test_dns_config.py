import pytest
from dnsconfigurator.dns_config import DNSConfig

@pytest.fixture
def config():
    config = DNSConfig("examples/sample_config.yaml")
    return config

# Test that constructor was called reading the config without problems
def test_read_config(config):
    assert isinstance(config, DNSConfig)

# Check that the 3 test domains exists
def test_domains(config):
    expected = ["example.com","mydomain.com","newdomain.com"]
    assert config.list() == expected

# Test the function to ensure data format of variables
def test_fix_type_with_list(config):
    input_data = [{"name": "test1", "value": "mx1.mail.com"}, {"name": "test2", "value": "mx2.mail.com"}]
    result = config.fix_type(input_data)
    # Since it's already a list, it should be returned as-is
    assert result == input_data

def test_fix_type_with_dict(config):
    input_data = {"test1": "mx1.mail.com", "test2": "mx2.mail.com"}
    expected_output = [{"name": "test1", "value": "mx1.mail.com"}, {"name": "test2", "value": "mx2.mail.com"}]
    result = config.fix_type(input_data)
    assert result == expected_output

def test_fix_type_with_none(config):
    input_data = None
    result = config.fix_type(input_data)
    # When input is None, should return an empty list
    assert result == []

def test_fix_type_with_invalid_type(config):
    input_data = "invalid string"
    with pytest.raises(ValueError, match=r"Invalid variable"):
        config.fix_type(input_data)
