from dnsconfigurator.dns_provider import DNSProvider
from dnsconfigurator.dns_record import DNSRecord
from dnsconfigurator.dns_domain import DNSDomain
import logging
from pprint import pprint
import code

logger = logging.getLogger(__name__)

class DNSProviderHetzner(DNSProvider):
    """DNS Provider implementation for Hetzner."""

    def setup(self):
        self.base = "https://dns.hetzner.com/api/v1"
        self.headers = {"Content-Type": "application/json", "Auth-API-Token": self.apikey}

    def get_zones(self):
        zonedata = self.req_get("zones")
        data = zonedata["zones"]
        for x in data:
            zone = {"id": x["id"], "name": x["name"], "created": x["created"], "modified": x["modified"]}
            self.zones[zone["name"]] = zone
        return zonedata

    def new_record(self, data):
        return DNSRecord({
          "id": data["id"],
          "type": data["type"],
          "name": data["name"],
          "value": self.unquote(data["value"]),
          "zone": data["zone_id"],
          "ttl": data.get("ttl",None),
          "created": data["created"],
          "modified": data["modified"]
        })

    def fetch(self):
        if not self.zoneid:
            raise ValueError("Cannot fetch. No domain specified")
        endpoint = f"records?zone_id={self.zoneid}"
        data = self.req_get(endpoint)
        for x in data["records"]:
            self.records.append(self.new_record(x))
        return self.records

    def assert_exist(self, record, action):
        if not record.id:
            raise ValueError(f"Cannot {action} record '{record}'. No ID in record")
        exists = self.req_get(f"records/{record.id}")
        if not exists:
            raise ValueError(f"Cannot {action} record '{record}'. Id does not exist at Hetzner")

    def record_data(self, record):
        return {"zone_id": record.zone, "type": record.type, "name": record.name, "value": record.value, "ttl": 3600}

    def update(self, record):
        self.assert_exist(record, "update")
        return self.req_put(f"records/{record.id}", data=self.record_data(record))

    def create(self, record):
        return self.req_post("records", data=self.record_data(record))

    def delete(self, record):
        self.assert_exist(record, "delete")
        return self.req_delete(f"records/{record.id}")
