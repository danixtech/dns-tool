## Overview ##
This will query DNS servers in order to compare the results world-wide.  You can
specify a specific server to use or you can leave it blank to automatically
query a preselected list of servers.

## Default DNS Server List ##
- 8.8.8.8 (google)
- 8.8.4.4 (google)
- 4.2.2.1 (Level 3)
- recpubns1.nstld.net
- resolver1.level3.net
- ordns.he.net
- resolver1.opendns.com
- resolver2.opendns.com

## Record Types ##
- A - IPv4 record
- AAAA - IPv6 record
- MX - Mail record
- PTR - Reverse DNS record
- SRV - Service Record
- TXT - Text file records

## Usage Examples ##
Query default list of nameservers

  ```python dns-tool.py -d example.com```

Query for a specific record type

  ```python dns-tool.py -d example.com -r A```

Query a specific DNS nameserver

  ```python dns-tool.py -d example.com -n resolver1.opendns.com```

Output to CSV file

  ```python dns-tool.py -d google.com -r MX --csv```

Ouptut to JSON file

  ```python dns-tool.py -d google.com -r TXT --json```

Query a specific nameserver

  ```python dns-tool.py -d google.com -r AAAA -n 8.8.8.8```

Adjust multi-threading for Query.  Allows for parallel queries

  ```python dns-tool.py -d google.com -r A --threads 10```

