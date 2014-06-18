DNS Web-UI
==========

A simple management interface for a single DNS server, built on Pyramid,
Bootstrap 3, DataTables and dnspython. This has only been tested with
BIND9, but should (in theory) support any DNS server that allows `AXFR`
transfer queries.

## Setup

Edit the `self.bind9` assignment in  `bind9ui/views.py` to point to your
server and use the zone you want to manage. By default, these are
`127.0.0.1` and `local`. After that, you can run the app with Pyramid's
`pserve`, or your production-ready server of choice. A sample
`pyramid.wsgi` file is provided; edit the path to point to your
installation if you decide to use that.

## Security

The app won't let you inject arbitrary record types (only `A` and
`CNAME` are allowed), and has some naive limits on other fields, but
that's about as far as it goes. There is no authentication, and it
assumes that your DNS server allows `AXFR` requests from anyone. You
should NOT be using this on a public-facing DNS server, or have the app
itself where just anyone can get to it. Put it on a trusted intranet to
get a pretty web interface for your local zone.

## Troubleshooting

```
...
    for name, node in z.nodes.items():
UnboundLocalError: local variable 'z' referenced before assignment
```

This means the server you're trying to use either doesn't exist, or
(perhaps more likely) doesn't allow zone transfers. This app was meant
to be used with a local DNS server that you manage yourself (and can
enable transfers for).
