#!/usr/bin/env python3
#
# dns-tool.py
#
# This will query DNS servers in order to compare the results world-wide.  You can specify a specific server to use or
# you can leave it blank to automatically query a preselected list of servers.
#
# Usage
# ex. python dns-tool.py -d example.com
#
# Notes
# 07-15-2025: This was mostly rewritten using the dns.resolver and prettytable modules
#
# Known Issues/ToDo
# - Put this in a GUI format (Django?)
# - Custom DNS server list that is importable
# - Query for multiple record types

#
# Intial Setup
#

# Import Modules
import argparse
import time
import socket
import csv
import json
import dns.resolver
import dns.exception
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of open dns server.  Note: Might change over time
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

# Currently supported and tested record types
supported_record_types = ['A', 'AAAA', 'MX', 'PTR', 'SRV', 'TXT']

# Check for arguments
def arg_check():
    parser = argparse.ArgumentParser(description='DNS query tool')
    parser.add_argument('-d', '--domain', required=True, help='Domain to query')
    parser.add_argument('-r', '--record', default='A', help='Record type: A, AAAA, MX, PTR, SRV, TXT')
    parser.add_argument('-n', '--nameserver', default='', help='Optional single nameserver to query')
    parser.add_argument('--csv', action='store_true', help='Output as CSV')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--threads', type=int, default=5, help='Number of threads (default 5)')
    return parser.parse_args()

# Resolve nameservers by IP
def resolve_ns_ip(ns):
    try:
        return socket.gethostbyname(ns)
    except socket.gaierror:
        return "Unresolved"

# DNS Query using dnsresolver
def dns_query(record_type, domain_name, dns_server):
    ns_ip = resolve_ns_ip(dns_server)
    if ns_ip == "Unresolved":
        return {
            "nameserver": dns_server,
            "nameserver_ip": ns_ip,
            "domain": domain_name,
            "record_type": record_type,
            "result": "Nameserver could not be resolved"
        }

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ns_ip]
    resolver.lifetime = 2.0
    resolver.timeout = 2.0

    try:
        # Check for existing CNAME record first
        cname_record = None
        try:
            cname_answer = resolver.resolve(domain_name, 'CNAME')
            cname_record = str(cname_answer[0])
        except dns.resolver.NoAnswer:
            pass

        answers = resolver.resolve(domain_name, record_type)
        results = []
        for rdata in answers:
            value = str(rdata)
            if cname_record and record_type not in ['CNAME', 'PTR']:
                value = f"{cname_record} A {value}"
                record_type = "CNAME"
            results.append({
                "nameserver": dns_server,
                "nameserver_ip": ns_ip,
                "domain": domain_name,
                "record_type": record_type,
                "result": value
            })
        return results

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout,
            dns.resolver.NoNameservers, dns.resolver.YXDOMAIN) as e:
        return {
            "nameserver": dns_server,
            "nameserver_ip": ns_ip,
            "domain": domain_name,
            "record_type": record_type,
            "result": f"Error: {str(e)}"
        }

def flatten_results(raw_results):
    flat = []
    for entry in raw_results:
        if isinstance(entry, list):
            flat.extend(entry)
        else:
            flat.append(entry)
    return flat

# Output the results as either json, csv or prettytable
def output_results(results, args):
    results = flatten_results(results)

    # Always print prettytable format
    table = PrettyTable(["Nameserver", "Nameserver IP", "Domain Name", "Record Type", "Result"])
    for row in results:
        table.add_row([
            row["nameserver"],
            row["nameserver_ip"],
            row["domain"],
            row["record_type"],
            row["result"]
        ])
    print("\nDNS Query Results for", args.domain, ":\n")
    print(table)

    # json format
    if args.json:
        #print(json.dumps(results, indent=2))
        with open("dns_output.json", "w") as f:
          json.dump(results, f, indent=2)
        print("Results written to dns_output.json")
    # csv format
    elif args.csv:
        writer = csv.DictWriter(
            open("dns_output.csv", "w", newline=''),
            fieldnames=["nameserver", "nameserver_ip", "domain", "record_type", "result"]
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)
        print("Results written to dns_output.csv")
    else:
      print("\nTo export these results into a structured file, add the `--csv` or `--json` flags.\n")

def main():
    # Argument parsing
    args = arg_check()
    domain = args.domain
    record_type = args.record.upper()

    # Check for supported record types
    if record_type not in supported_record_types:
        print(f"Unsupported record type '{record_type}'. Supported: {', '.join(supported_record_types)}")
        return

    # Custom DNS servers or default server list?
    dns_servers = [args.nameserver] if args.nameserver else dns_default_list

    # Run the DNS query using multithreading
    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(dns_query, record_type, domain, ns) for ns in dns_servers]
        for future in as_completed(futures):
            results.append(future.result())

    # Display the results
    output_results(results, args)


if __name__ == '__main__':
    main()

#
# vim: set syntax=python
#
