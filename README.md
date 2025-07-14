## Overview ##
This will query DNS servers in order to compare the results world-wide.  You can
specify a specific server to use or you can leave it blank to automatically 
query a preselected list of servers.

## Default DNS Server List ##
- 8.8.8.8 (google)
- 8.8.4.4 (google)
- 4.2.2.1 (Level 3)
- recpubns1.nstld.net
- ns1.exetel.com.au
- resolver1.level3.net
- ordns.he.net
- safe.dns.yandex.ru
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
Query default list

  ```python dns-tool.py -d example-domain.com```

Query for a specific record

  ```python dns-tool.py -d example-domain.com -r A```

Query a specific DNS server

  ```python dns-tool.py -d example-domain.com -n ns.galois.com```

