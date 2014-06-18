import re
import exceptions

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

from bind9ui import BIND9


class DNSViews(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        self.bind9 = BIND9('127.0.0.1', 'local')
        self.records = self.bind9.dump()
        self.sortedRecords = self.bind9.sortedRecords()

    @view_config(route_name='dns_view',
            renderer='templates/dns_view.pt',
            request_method='GET')
    def dns_view(self):
        return dict(title='DNS Records', records=self.sortedRecords)

    @view_config(route_name='dns_view',
            renderer='templates/dns_view.pt',
            request_method='POST')
    def dns_newhost(self):
        hostname = str(self.request.POST['hostname'])
        url = self.request.route_url('dns_addedit', hostname=hostname)
        return HTTPFound(url)

    @view_config(route_name='dns_addedit',
            renderer='templates/dns_addedit.pt',
            request_method='GET')
    def dns_addedit(self):
        hostname = self.request.matchdict['hostname']
        try:
            record = self.records[hostname]
        except:
            record = {
                'type': None,
                'resolveto': None,
                'ttl': 86400,
            }
        
        return dict(title='DNS Record for %s' % hostname,
                record=record, hostname=hostname, error=None)

    @view_config(route_name='dns_addedit',
            renderer='templates/dns_addedit.pt',
            request_method='POST')
    def process_form(self):
        hostname = self.request.matchdict['hostname']

        # Default values
        try:
            record = self.records[hostname]
        except:
            record = {
                'hostname': hostname,
                'type': None,
                'resolveto': None,
                'ttl': 86400
            }

        if 'submit' in self.request.params:
            try:
                record = {
                    'hostname': str(self.request.POST['hostname']),
                    'type': str(self.request.POST['rtype']),
                    'resolveto': str(self.request.POST['resolveto']),
                    'ttl': int(self.request.POST['ttl']),
                }
                # Max TTL per RFC 2181, 2147483647
                if record['ttl'] < 0 or record['ttl'] > 2147483647:
                    raise Exception("TTL out of bounds")
                elif record['type'] not in ['A', 'CNAME']:
                    raise Exception("Invalid record type")
                elif not re.match(
                        '^([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9])$',
                        record['hostname']
                    ):
                    raise Exception("Invalid hostname")
                elif (record['type'] == 'A' and 
                     not re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
                        record['resolveto'])):
                    raise Exception(
                        "'A' records must point to a valid IPv4 address"
                    )
                elif (record['type'] == 'CNAME' and
                     record['resolveto'] not in self.records):
                    raise Exception(
                        "'CNAME' records must point to existing hostname"
                    )
            except Exception as e:
                if type(e) is exceptions.ValueError and 'int' in e.message:
                    error = "TTL must be a valid integer value"
                else:
                    error = e.message
                # Form doesn't validate.
                return dict(title='DNS Record for %s' % hostname,
                    record=record, hostname=hostname, error=error)

            # Form validates, update the DNS server.
            try:
                self.bind9.update(
                        hostname,            # hostname
                        record['hostname'],  # newhostname
                        record['ttl'],       # ttl
                        record['type'],      # rtype
                        record['resolveto']  # resolveto
                )
            except Exception as e:
                # Probably a network error.
                return dict(title='DNS Record for %s' % hostname,
                    record=record, hostname=hostname, 
                    error="Bind9 error: "+e.message)
        elif 'delete' in self.request.params:
            try:
                self.bind9.delete(hostname)
            except:
                return dict(title='DNS Record for %s' % hostname,
                        record=record, hostname=hostname, 
                        error="Bind9 error: "+e.message)

        # Go back to the homepage.
        url = self.request.route_url('dns_view')
        return HTTPFound(url)
