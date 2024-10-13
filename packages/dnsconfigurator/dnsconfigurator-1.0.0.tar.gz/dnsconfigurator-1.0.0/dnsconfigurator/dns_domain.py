import logging
from dnsconfigurator.dns_record import DNSRecord
from dnsconfigurator.dns_provider import DNSProviderFactory

logger = logging.getLogger(__name__)

class DNSDomain:
    def __init__(self, name):
        self.provider = ""
        self.id       = None
        self.name     = name
        self.ip       = ""
        self.records  = []
        self.api      = ""
        self.remotes  = []

        self.add      = []
        self.delete   = []
        self.update   = []

    def new_record(self, data):
        self.records.append(DNSRecord(data))

    def add_record(self, type, name, value):
        record = DNSRecord({"type": type.upper(), "name": name, "value": value})
        record.zone = self.id
        self.records.append(record)
        return record

    def add_a(self, name, value):
        return self.add_record("A", name, value)

    def add_cname(self, name, value):
        if value in ["~",None,"@"]:
            value = self.name
        return self.add_record("CNAME", name, self.dot(self.placeholder(value)))

    def add_txt(self, name, value):
        if name in ["~",None,"@"]:
            name = "@"
        return self.add_record("TXT", name, self.placeholder(value))

    def add_mx(self, priority, value):
        return self.add_record("MX", "@", f"{priority} {self.dot(value)}")

    def placeholder(self, field):
        return field.replace("{DOMAIN}", self.name)

    def dot(self, v):
        return v if v.endswith(".") else v+"."

    def connect(self):
        if not self.api:
            self.api = DNSProviderFactory.create_provider(self.provider)
            self.api.set_domain(self.name)
            self.id = self.api.zoneid

    def fetch(self):
        logger.debug(f"Fetch remote config on {self.provider} for '{self.name}'")
        self.connect()
        self.remotes = self.api.fetch()
        for x in self.records:
            x.zone = self.id
        self.remotes.sort(key = lambda x: (x.type, x.name))

    def compare(self):
        logger.debug(f"Comparing local and remote records for '{self.name}'")
        if not self.records:
            raise ValueError(f"No local records for domain")
        if not self.remotes:
            raise ValueError(f"No remote records for domain")

        to_add    = []
        to_delete = []
        to_edit   = []

        # Convert lists to dictionaries with the record's name (and type if needed) as the key
        record_dict = self._group_records(self.records)
        remote_dict = self._group_records(self.remotes)

        # Process records to delete and edit
        for key, remote_record in remote_dict.items():
            if key not in record_dict:
                to_delete.append(remote_record)
            else:
                desired_record = record_dict[key]
                if self._needs_update(desired_record, remote_record):
                    to_edit.append((desired_record, remote_record))

        # Process records to add
        for key, desired_record in record_dict.items():
            if key not in remote_dict:
                to_add.append(desired_record)

        self.add    = to_add
        self.delete = to_delete
        self.update = to_edit

        return to_add, to_delete, to_edit

    def uptodate(self):
        return not (self.add or self.delete or self.update)

    def _group_records(self, records):
        """Helper function to group records by key depending on type."""
        grouped_records = {}
        for record in records:
            if record.type == "A" and record.name == "localhost":
                logger.debug("Skipping localhost A record")
                continue
            if record.type in ["SOA", "NS"]:
                logger.debug("Skipping SOA/NS records")
                continue
            if record.type in ['A', 'CNAME']:
                key = f"{record.name}_{record.type}"
            elif record.type == 'MX':
                # Assuming value is "priority target"
                key = f"{record.name}_{record.type}_{record.value.split(' ')[1]}"  
            elif record.type == 'TXT':
                # Use whole record as key = never update, just add/delete
                key = f"{record.name}_{record.type}_{record.value}"
            else:
                logger.warning(f"Unknown record type: {record.type}")
                key = f"{record.name}_{record.type}"
            grouped_records[key] = record
        return grouped_records

    def _needs_update(self, desired_record, remote_record):
        """Helper function to determine if a record needs to be updated."""
        if desired_record.type != remote_record.type:
            return True
        if desired_record.value != remote_record.value:
            return True
        return False

    def sync(self, dryrun):
        if self.delete or self.add or self.update:
            logger.info("Updating remote configuration to reflect local configuration")
        else:
            logger.info("Nothing to sync")
            return
        for record in self.delete:
            logger.info(f"Deleting remote {record.type:5} record: {record.name:5} = {record.value}")
            if dryrun:
                logger.warning(f"Dryrun: Would have deleted record {record.id}")
            else:
                self.api.delete(record)
        for record in self.add:
            logger.info(f"Creating remote {record.type:5} record: {record.name:5} = {record.value}")
            if dryrun:
                logger.warning(f"Dryrun: Would have added {record.type} reoord '{record.name}'")
            else:
                self.api.create(record)
        for (new, old) in self.update:
            if not new.id:
                new.id = old.id
            if dryrun:
                logger.warning(f"Dryrun: Would have updated {record.type} reoord '{record.id}'")
            else:
                self.api.update(new)
            logger.info(f"Updating remote {new.type:5} record: {new.name} changed from {old.value} to {new.value}")


    def show(self, show="records"):
        retval=f"Domain '{self.name}'\n"
        retval+=f"  Provider: {self.provider}\n"
        for x in getattr(self,show):
            retval+=f"  {x.type:6}: {x.name:10} = {x.value}\n"
        return retval

    def __str__(self):
        return self.show()
