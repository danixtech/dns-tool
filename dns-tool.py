#!/usr/bin/python3
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

# Variables
dns_default_list = [
	"8.8.8.8", \
	"8.8.4.4", \
	"4.2.2.1", \
	"recpubns1.nstld.net", \
	"ns1.exetel.com.au", \
	"resolver1.level3.net", \
	"ordns.he.net", \
	"safe.dns.yandex.ru", \
	"resolver1.opendns.com", \
	"resolver2.opendns.com" \
]

# Import Modules
import argparse, subprocess, time

# Check for arguments
def arg_check():
	parser = argparse.ArgumentParser(prog='dns-tool.py')
	parser.add_argument('-r', '--record', default='A', required=False, action='store', dest='record_type', help='A, AAAA, MX, PTR, SRV, TXT')
	parser.add_argument('-d', '--domain', default='', required=True, action='store', dest='domain_name', help='Requires a valid domain name ex. google.com')
	parser.add_argument('-n', '--nameserver', default='', required=False, action='store', dest='nameserver', help='Optional nameserver to query')
	args = vars(parser.parse_args())
	record_type = str(args['record_type'])
	domain_name = str(args['domain_name'])
	nameserver = str(args['nameserver'])
	return record_type, domain_name, nameserver

# DNS Query Function
def dns_query(record_type, domain_name, nameserver):
	# Check for supplied nameserver
	if nameserver != "":
		# Use supplied nameserver
		dns_server_list = [nameserver]
	else:
		# Use default nameserver list
		dns_server_list = dns_default_list

	# Loop through dns_server list
	for dns_server in dns_server_list:
		query_command = "dig +noall +answer " + record_type + " @" + dns_server + " " + domain_name
		print("Name Server: " + dns_server)
		result = subprocess.Popen(query_command, shell=True)
		#print(query_command)
		time.sleep(1)

# Main function
def main():
	# Check optional Arguments
	record_type, domain_name, nameserver = arg_check()
	
	# Query DNS server
	dns_query(record_type, domain_name, nameserver)

#
# Main
#

main()

#
# eof
#
