#!/usr/bin/env python

import os
import re
from prettytable import PrettyTable

# Configuration
nmap_output_path = "./nmap_output.txt"
dictionary_ref_path = "./dictionary_reference.txt"

ip_range = "10.0.0.1-20"
ip_range_regex = "10\.0\.0\.(.*)"
local_ip = "10.0.0.8"
local_mac = "B8:27:EB:AA:C3:AA"

os.system("echo 'Beginning Scan...'")
os.system("sudo nmap -sP " + ip_range + " > " + nmap_output_path)

# This, of course, is the output from Nmap
nmap = open(nmap_output_path, "r")

# This is where we get the Hostname/MAC address combos
dictionary_ref = open(dictionary_ref_path, "r")

ip_addresses = []
mac_addresses = []
match_ip_var = "cats"
mac_and_hostnames = {}

for line in dictionary_ref:
   mac, hostname = line.strip().split('=')
   mac_and_hostnames[mac.strip()] = hostname.strip()
dictionary_ref.close()

for line in nmap:

   match_ip = re.search(ip_range_regex, line) # This regex, of course, needs to be modified to suit your own IP structure.
   match_mac = re.search("..:..:..:..:..:..", line)

   if match_ip:
      ip_addresses.insert(0, match_ip.group(0))
      match_ip_var = match_ip.group(0)

# For some reason the rPi's own MAC address doesn't register.
# This manually ads it in when it's static ip is detected

   elif match_ip_var == local_ip:
      mac_addresses.insert(0, local_mac)

   if match_mac:
      mac_addresses.insert(0, match_mac.group(0))

nmap.close()

# The string is used to display the number on one line
# The integer is used in the for statement below

number_hosts_int = len(mac_addresses)
number_hosts_str = str(number_hosts_int)

x=PrettyTable(["Hostname", "MAC", "IP"])
x.align["Hostname", "MAC", "IP"] = "c"
x.padding_width = 1

for i in xrange(0,number_hosts_int,1):
   if mac_addresses[i] in mac_and_hostnames:
      current_hostname = mac_and_hostnames[mac_addresses[i]]
   else:
      current_hostname = "UNKNOWN"
   x.add_row([current_hostname, mac_addresses[i], ip_addresses[i]])

print x
print "Number of Hosts: " + number_hosts_str
