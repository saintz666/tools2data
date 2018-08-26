###
# Name:    pcap_parse01.py
# Description: Parsing PCAP with double base64 decode
# Author:      SAINTz
# Twitter: @__SAINTz__
# License:     GNU/GPL
##


from scapy.all import *
import urllib
import base64
import time
import sys
timer = time.time()

def main():
	packets = rdpcap(sys.argv[1])
	fo = open(sys.argv[2],'w+')

	print "Parsing %s - Total %s packets" % (sys.argv[1],len(packets))

	for p in xrange(len(packets)):
		if (packets[p].dport == 80 or packets[p].sport == 80) and (packets[p][1].dst=="172.16.244.10"):
			try:
				packets[p].load
			except AttributeError:
				continue

			if "hello=" in packets[p].load:
				#print packets[p].load
				encryted_1 = urllib.unquote(packets[p].load.split("&")[-2].split("=")[1]).decode('utf8')
				#encryted_1 = urllib.unquote(packets[p].load).decode('utf8').split("&")[-2].split("=")[1]
				fo.write(super_base64(encryted_1))
				fo.write("\n")
				encryted_1 = urllib.unquote(packets[p].load.split("&")[-1].split("=")[1]).decode('utf8')
				encryted_1 = base64.decodestring(encryted_1).split("=")[1].strip()
				#print super_base64(urllib.unquote(encryted_1).decode('utf8'))
				fo.write(super_base64(urllib.unquote(encryted_1).decode('utf8')))
				fo.write("\n")
			else:
				encryted_1 = urllib.unquote(packets[p].load).decode('utf8')
				encryted_1=  super_base64(encryted_1)
				#print super_base64(encryted_1)
				fo.write(super_base64(encryted_1))
				fo.write("\n")

				#print p
				#flags = p.sprintf("%TCP.flags%")
				#if flags == 'PA':
				#	print p
				#print p.load
	fo.close()
	print "Parse completed %s seconds" % (time.time()-timer)

def super_base64(data):
	passme = 0
	while(1):
		try:
			missing_padding = len(data) % 4
			if missing_padding != 0:
				data += '='* (4 - missing_padding)
			data_rtn = base64.decodestring(data).strip()
			break
		except Exception,err:
			for x in xrange(-1,-15,-1):
				try:
					data_rtn = base64.decodestring(data[:x]).strip()
					passme = 1
					break
				except Exception, err:
					#print err
					pass

			if passme == 1:
				break

	#encryted_1 = base64.decodestring(encryted_1[:-2]).strip()
	return data_rtn

if __name__ == "__main__":
   main()
