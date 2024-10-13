class DNSRecord:

    def __init__(self, data={}):
        self.id       = ""
        self.type     = ""
        self.name     = ""
        self.value    = ""
        self.zone     = ""
        self.ttl      = ""
        self.created  = ""
        self.modified = ""
        for x in data:
            if not hasattr(self, x):
                raise ValueError(f"Cannot create DNSrecord. Invalid record data: {x}")
            setattr(self,x,data[x])

    def fill(self, type, name, value):
        self.type=type
        self.name=name
        self.value=value
        return self

    def A(self, name, value):
        self.fill("A", name, value)
        return self

    def CNAME(self, name, value):
        self.fill("CNAME", name, value)
        return self

    def TXT(self, name, value):
        self.fill("TXT", name, value)
        return self

    def MX(self, priority, value):
        self.fill("MX", "@", f"{priority} {value}")
        return self

    def __str__(self):
        return(f"{self.type}: {self.name}={self.value}")
