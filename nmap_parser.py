#!/usr/bin/env python

import os
import re
from prettytable import PrettyTable

os.system("echo 'Beginning Scan...'")
os.system("sudo nmap -sP 10.0.0.1-20>~/Soundoff/nmap_output.txt")

# This, of course, is the output from Nmap
nmap = open("~/Soundoff/nmap_output.txt","r")

# This is where we get the Hostname/MAC address combos
dictionary_ref = open("~/Soundoff/dictionary_reference.txt", "r")

ip_addresses = []
mac_addresses = []
match_ip_var = "cats"
mac_and_hostnames = {}

for line in dictionary_ref:
   mac, hostname = line.strip().split('=')
   mac_and_hostnames[mac.strip()] = hostname.strip()
dictionary_ref.close()

for line in nmap:

   match_ip = re.search("10\.0\.0\.(.*)", line) # This regex, of course, needs to be modified to suit your own IP structure.
   match_mac = re.search("..:..:..:..:..:..", line)

   if match_ip:
      ip_addresses.insert(0, match_ip.group(0))
      match_ip_var = match_ip.group(0)

# For some reason the rPi's own MAC address doesn't register.
# This manually ads it in when it's static ip is detected

   elif match_ip_var == "10.0.0.8":
      mac_addresses.insert(0, "B8:27:EB:AA:C3:AA")

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
