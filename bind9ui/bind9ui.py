from dns import zone, query, update
from dns.rdataclass import *
from dns.rdatatype import *

class BIND9(object):
    def __init__(self, server, domain):
        self.server = server
        self.domain = domain
        self.records = {}

    def dump(self):
        try:
            z = zone.from_xfr(query.xfr(self.server, self.domain,
                        timeout=10))
        except:
            print "Exception in bind9.BIND9.dump() on zone xfr"

        for name, node in z.nodes.items():
            if str(name) == '@': continue
            rdatasets = node.rdatasets
            for rdataset in rdatasets:
                if rdataset.rdclass == IN and rdataset.rdtype in [A, CNAME]:
                    record = str(rdataset).split(' ')
                    self.records[str(name)] = {
                        'ttl': record[0],
                        'type': record[2],
                        'resolveto': record[3],
                        }
        return self.records

    def sortedRecords(self):
        """Converts the self.records dict to a list of tuples, sorted by
        the tuple's first element.
        """
        return sorted(self.records.items())

    def update(self, hostname, newhostname, ttl, rtype, resolveto):
        """Throws all exceptions upstream."""
        nsupdate = update.Update(str(self.domain))
        nsupdate.delete(str(hostname))
        nsupdate.delete(str(newhostname))
        nsupdate.add(str(newhostname), int(ttl), str(rtype),
                str(resolveto))
        query.udp(nsupdate, self.server)

    def delete(self, hostname):
        """Throws all exceptions upstream."""
        nsupdate = update.Update(str(self.domain))
        nsupdate.delete(str(hostname))
        query.udp(nsupdate, self.server)
