#!/usr/bin/env python3
#
# dns-tool.py
#
# This will query DNS servers in order to compare the results world-wide.  You can specify a specific server to use or
# you can leave it blank to automatically query a preselected list of servers.
#
# Usage
# ex. python dns-tool.py -d example-domain.com
#
# Notes
# Anything special you want to add.
#
# Known Issues/ToDo
# - Add a delay when waiting for a response
# - Put this in a GUI format

#
# Intial Setup
#

# Import Modules
import argparse
import time
import dns.resolver
from prettytable import PrettyTable

# Default DNS resolvers
dns_default_list = [
    "8.8.8.8",
    "8.8.4.4",
    "4.2.2.1",
    "recpubns1.nstld.net",
    "resolver1.level3.net",
    "ordns.he.net",
    "resolver1.opendns.com",
    "resolver2.opendns.com"
]

# Check for arguments
def arg_check():
    parser = argparse.ArgumentParser(prog='dns-tool.py')
    parser.add_argument('-r', '--record', default='A', required=False,
                        help='A, AAAA, MX, PTR, SRV, TXT')
    parser.add_argument('-d', '--domain', required=True,
                        help='Domain to query, e.g. google.com')
    parser.add_argument('-n', '--nameserver', required=False, default='',
                        help='Optional single nameserver to query (IP or hostname)')
    return parser.parse_args()

# DNS Query Function using dnspython
def dns_query(record_type, domain_name, dns_servers):
    results = []

    for dns_server in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server] if not dns_server.endswith('.net') else []
        resolver.nameserver = dns_server  # for hostnames
        resolver.lifetime = 2.0
        resolver.timeout = 2.0

        print(f"Querying: {dns_server}")
        try:
            # For hostnames like recpubns1.nstld.net, we need to resolve it first
            if not dns_server.replace('.', '').isdigit():
                dns_server_ip = dns.resolver.resolve(dns_server, 'A')[0].to_text()
                resolver.nameservers = [dns_server_ip]
            answers = resolver.resolve(domain_name, record_type)
            for rdata in answers:
                results.append((dns_server, record_type, str(rdata)))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout,
                dns.resolver.NoNameservers, dns.resolver.YXDOMAIN) as e:
            results.append((dns_server, record_type, f"Error: {str(e)}"))
        time.sleep(0.5)  # small delay between queries

    return results

# Main function
def main():
    args = arg_check()

    record_type = args.record.upper()
    domain_name = args.domain
    nameserver = args.nameserver

    if nameserver:
        dns_servers = [nameserver]
    else:
        dns_servers = dns_default_list

    results = dns_query(record_type, domain_name, dns_servers)

    # Display results with PrettyTable
    table = PrettyTable(["DNS Server", "Record Type", "Result"])
    for res in results:
        table.add_row(res)

    print("\nDNS Query Results:")
    print(table)

# Run the script
if __name__ == '__main__':
    main()

#
# vim: set syntax=python
#
