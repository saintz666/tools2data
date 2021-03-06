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
    parser = argparse.ArgumentParser(description="Parse ZoneFiles output and reconstruct list of domains")
    parser.add_argument('inputfile', help='The Zone File')
    parser.add_argument('outputfile', help='The output filename')
    args = parser.parse_args()
    inputfile_01=args.inputfile
    outputfile_02= args.outputfile

    if os.path.isdir(inputfile_01):
        files = os.listdir(inputfile_01)
        print "Directory Path provided - "
        for name in files:
            print "Processing %s \n" % (name)
            process_file(os.path.join(inputfile_01, name),outputfile_02)

    elif os.path.isfile(inputfile_01):
        print "Processing %s \n" % (inputfile_01)
        process_file(inputfile_01,outputfile_02)

    else:
        print "Error"



def process_file(inputfile,outputfile):
    try:
        fi = open(inputfile,'r+')
        fi2 = fi.readlines()
        fi.close()
        report = []
        fo = open(outputfile, 'a+')
        current_domain=''
        for x in xrange(len(fi2)):
            if ("$ORIGIN" in fi2[x]):
                if ("$ORIGIN ." not in fi2[x]) and ("$ORIGIN _" not in fi2[x]):
                    current_domain = sanitize_trailing(fi2[x].split(' ')[1].strip())
                else:
                    current_domain = ''

            elif ("\tA\t" in fi2[x]) or ("\tCNAME\t" in fi2[x]):
                if  len(current_domain) < 2:
                    continue
                else:
                    subdomain_domain = fi2[x].split('\t')[0].strip()
                    record_domain =  sanitize_trailing(fi2[x].split('\t')[-1].strip())

                    out = current_domain+","+subdomain_domain+"."+current_domain+","+record_domain+"\n"
                    if len(out) > 10: 
                        fo.write(out)


        fo.close()

    except IOError as e:
        print "IO error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(2)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        sys.exit(2)

def sanitize_trailing(data):
    try:
        if data[-1:] == ".":
            return data[:-1]
        else:
            return data
    except Exception, err:
        #print "Unexpected error:", sys.exc_info()[0]
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        #sys.exit(2)
        return data


if __name__ == "__main__":
   main(sys.argv)
