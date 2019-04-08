#!/bin/python

## The following uses blockstack_zones library

import blockstack_zones
import sys

dat = None
with open(sys.argv[1], "r") as f:
    dat = f.read()
    f.close()

site=[]
temp_site= ""

dns = blockstack_zones.parse_zone_file(dat)
for xx in xrange(len(dns['a'])):
	if (dns['a'][xx]['name'] != "@") and (dns['a'][xx]['name'] != "."):
		temp_site =  "%s.%s" % (dns['a'][xx]['name'],sys.argv[1])
		temp_site = temp_site.replace("#","").replace("_","")
		if temp_site not in site:
			print temp_site
			site.append(temp_site)

for xx in xrange(len(dns['cname'])):
	if (dns['cname'][xx]['name'] != "@") and (dns['cname'][xx]['name'] != "."):
		temp_site =  "%s.%s" % (dns['cname'][xx]['name'],sys.argv[1])
		temp_site = temp_site.replace("#","").replace("_","")
		if temp_site not in site:
			print temp_site
			site.append(temp_site)

for x in xrange(len(site)):
	print site[x]
