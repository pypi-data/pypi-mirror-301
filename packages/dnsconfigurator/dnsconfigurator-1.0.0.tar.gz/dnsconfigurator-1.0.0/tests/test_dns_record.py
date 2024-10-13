import pytest
from dnsconfigurator.dns_record import DNSRecord

def test_initialization_empty():
    record = DNSRecord()
    assert record.id == ""
    assert record.type == ""
    assert record.name == ""
    assert record.value == ""
    assert record.zone == ""
    assert record.ttl == ""
    assert record.created == ""
    assert record.modified == ""

def test_initialization_with_data():
    data = {"type": "A", "name": "example.com", "value": "192.168.1.1"}
    record = DNSRecord(data)
    assert record.type == "A"
    assert record.name == "example.com"
    assert record.value == "192.168.1.1"

def test_invalid_data_raises_exception():
    with pytest.raises(ValueError):
        DNSRecord({"invalid_field": "value"})

def test_fill_method():
    record = DNSRecord()
    record.fill("A", "example.com", "192.168.1.1")
    assert record.type == "A"
    assert record.name == "example.com"
    assert record.value == "192.168.1.1"

def test_A_method():
    record = DNSRecord().A("example.com", "192.168.1.1")
    assert record.type == "A"
    assert record.name == "example.com"
    assert record.value == "192.168.1.1"

def test_CNAME_method():
    record = DNSRecord().CNAME("www.example.com", "example.com")
    assert record.type == "CNAME"
    assert record.name == "www.example.com"
    assert record.value == "example.com"

def test_TXT_method():
    record = DNSRecord().TXT("example.com", "v=spf1 include:_spf.example.com ~all")
    assert record.type == "TXT"
    assert record.name == "example.com"
    assert record.value == "v=spf1 include:_spf.example.com ~all"

def test_MX_method():
    record = DNSRecord().MX(10, "mail.example.com")
    assert record.type == "MX"
    assert record.name == "@"
    assert record.value == "10 mail.example.com"

def test_str_method():
    record = DNSRecord().A("example.com", "192.168.1.1")
    assert str(record) == "A: example.com=192.168.1.1"

