from dnsconfigurator.dns_provider import DNSProvider
from dnsconfigurator.dns_record import DNSRecord
from dnsconfigurator.dns_domain import DNSDomain
import logging
from pprint import pprint
import code
import os
import re

logger = logging.getLogger(__name__)

class DNSProviderCloudflare(DNSProvider):
    """DNS Provider implementation for Cloudflare."""

    def setup(self):
        self.base = "https://api.cloudflare.com/client/v4"
        self.dnsmail = os.getenv("EMAIL")
        if self.dnsmail is None:
            raise ValueError("No email address for cloudflare")
        self.headers = {"Content-Type": "application/json", "X-Auth-Key": self.apikey, "X-Auth-Email": self.dnsmail}

    def get_zones(self):
        zonedata = self.req_get("zones")
        data = zonedata["result"]
        for x in data:
            zone = {"id": x["id"], "name": x["name"], 
                    "status": x["status"],
                    "created": x["created_on"], 
                    "modified": x["modified_on"]}
            if not zone["status"] == "active":
                debug.error(f"Cloudflare domain {x['name']} is not active")
            self.zones[zone["name"]] = zone
        return zonedata

    def new_record(self, data):
        if (data["type"] == "MX"):
            data["content"] = f"{data['priority']} {data['content']}"
        if (data["type"] in ["MX","CNAME"]):
            data["content"] += "."
        return DNSRecord({
          "id": data["id"],
          "type": data["type"],
          "name":  re.sub(rf"{self.domain}","@",data["name"]).replace(".@",""),
          "value": self.unquote(data["content"]),
          "zone": data["zone_id"],
          "ttl": data.get("ttl",None),
          "created": data["created_on"],
          "modified": data["modified_on"]
        })

    def fetch(self):
        if not self.zoneid:
            raise ValueError("Cannot fetch. No domain specified")
        endpoint = f"zones/{self.zoneid}/dns_records"
        data = self.req_get(endpoint)
        for x in data["result"]:
            self.records.append(self.new_record(x))
        return self.records

    def assert_exist(self, record, action):
        if not record.id:
            raise ValueError(f"Cannot {action} record '{record}'. No ID in record")
        exists = self.req_get(f"zones/{self.zoneid}/dns_records/{record.id}")
        if not exists:
            raise ValueError(f"Cannot {action} record '{record}'. Id does not exist at Hetzner")

    def record_data(self, record):
        if record.type=="MX":
            return self.mx_record_data
        data = {"type": record.type, "name": record.name, "content": record.value, "ttl": 3600}
        if record.type in ["A","CNAME"]:
            data["proxied": True]
        return data

    def mx_record_data(self, record):
        (priority,host) = priority=record.value.split(" ")
        return {"type": "MX", "name": record.name, "content": host, "priority": priority, "ttl": 3600}

    def update(self, record):
        self.assert_exist(record, "update")
        return self.req_patch(f"zones/{self.zoneid}/dns_records/{record.id}", data=self.record_data(record))

    def create(self, record):
        return self.req_post(f"zones/{self.zoneid}/dns_records", data=self.record_data(record))

    def delete(self, record):
        self.assert_exist(record, "delete")
        return self.req_delete(f"zones/{self.zoneid}/dns_records/{record.id}")
