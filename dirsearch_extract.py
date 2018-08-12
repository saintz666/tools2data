#!/usr/bin/python
'''
Author: SAINTz
Twitter: @__SAINTz__
'''

import sys,os
import argparse

def main(argv):
	inputfile = ''
	outputfile = ''
	parser = argparse.ArgumentParser(description="Parse Dirsearch output and locate HTTP Code 200")
	parser.add_argument('inputfile', help='The Dirsearch report')
	parser.add_argument('outputfile', help='The output filename')
	args = parser.parse_args()
	inputfile=args.inputfile
	outputfile = args.outputfile

	http_code_to_view = ['200','500']
	
	try:
		fi = open(inputfile,'r+')
		fi2 = fi.readlines()
		fi.close()
		report = []
		fo = open(outputfile, 'a+')
		for x in xrange(len(fi2)):
			httpcode = ''
			httpcode = fi2[x].split('   ')[0].strip()
			if httpcode in http_code_to_view:
				out = fi2[x].split('   ')[2].strip() + "\n"
				fo.write(out)

		fo.close()
	except IOError as e:
		print "IO error({0}): {1}".format(e.errno, e.strerror)
		sys.exit(2)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		#exc_type, exc_obj, exc_tb = sys.exc_info()
		#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#print(exc_type, fname, exc_tb.tb_lineno)
		sys.exit(2)

	
if __name__ == "__main__":
   main(sys.argv)
