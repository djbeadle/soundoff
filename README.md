Soundoff should live in a folder named, “Soundoff” in your home directory. When Soundoff is run by ./soundoff the bash script runs a basic nmap ping scan of the first 30 IP’s on the network and outputs which respond to the file, “nmap_output.txt”. The python script then parses that file and matches the MAC addresses to a predefined list of hostnames. Unrecognized hostnames are marked as, “UNKNOWN”

![Soundoff in Action](http://i.imgur.com/MR7FTbb.png)

To make Soundoff work on your system:

1) Change the ip address range in soundoff.sh to the appropriate values

2) Populate dictionary_reference.txt with your hostnames. The format should be, “00:11:22:33:44:55=Hostname” with only one entry per line. 

3) OPTIONAL: Add a bash alias so you can run Soundoff from a simple command anywhere. My entry looks like: “alias soundoff=~/soundoff/soundoff.sh”

Soundoff requires the python library prettytable which can be found here: https://code.google.com/p/prettytable/ . It also requires nmap to be installed. 
