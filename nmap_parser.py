#!/usr/bin/env python

import os
import re
import sys
from prettytable import PrettyTable

# Paths
script_root_directory = sys.path[0]
nmap_output_path = script_root_directory + "/nmap_output.txt"
dictionary_ref_path = script_root_directory + "/dictionary_reference.txt"

# Configuration
ip_range = "10.0.0.1-20"
ip_range_regex = "10\.0\.0\.(.*)" # This regex, of course, needs to be modified to suit your own IP structure.
local_ip = "10.0.0.8"
local_mac = "B8:27:EB:AA:C3:AA"

os.system("echo 'Beginning Scan...'")
os.system("sudo nmap -sP " + ip_range + " > " + nmap_output_path)

# This, of course, is the output from Nmap
nmap = open(nmap_output_path, "r")

ip_addresses = []
mac_addresses = []
match_ip_var = None

for line in nmap:
   match_ip = re.search(ip_range_regex, line)
   match_mac = re.search("..:..:..:..:..:..", line)
   if (not match_ip) and (not match_mac):
      continue

   if match_ip:
      ip_addresses.insert(0, match_ip.group(0))
      match_ip_var = match_ip.group(0)
   elif match_ip_var == local_ip:
      # For some reason the rPi's own MAC address doesn't register.
      # This manually ads it in when it's static ip is detected
      mac_addresses.insert(0, local_mac)

   if match_mac:
      mac_addresses.insert(0, match_mac.group(0))

nmap.close()

# This is where we get the Hostname/MAC address combos
dictionary_ref = open(dictionary_ref_path, "r")
mac_and_hostnames = {}
for line in dictionary_ref:
   mac, hostname = line.strip().split('=')
   mac_and_hostnames[mac.strip()] = hostname.strip()
dictionary_ref.close()

table = PrettyTable(["Hostname", "MAC", "IP"])
table.align["Hostname", "MAC", "IP"] = "c"
table.padding_width = 1

number_hosts = len(mac_addresses)
for i in xrange(0, number_hosts, 1):
   if mac_addresses[i] in mac_and_hostnames:
      current_hostname = mac_and_hostnames[mac_addresses[i]]
   else:
      current_hostname = "UNKNOWN"
   table.add_row([current_hostname, mac_addresses[i], ip_addresses[i]])

print table
print "Number of Hosts: " + str(number_hosts)
