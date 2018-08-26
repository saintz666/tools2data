###
# Name:    DumpMyCred
# Description: Credential Dump Parser script
# Author:      SAINTz
# Version:     0.1 - 12 December 2017
# License:     GNU/GPL
##

import pymongo
import os
import sys
import datetime
import time
import logging

timer = time.time()
try:
    client = pymongo.MongoClient("localhost", 27017)
    db=client.credd2
except Exception,err:
    logging.info(err)
    sys.exit()

filecounter=0

stupid_pass= ["gayASSfagpastebinleaks","plaintext_password",""]
stupid_pass_keyword = ['pastebin.com/u']
logging.basicConfig(format='%(asctime)s - %(message)s',filename='mongo_search_usernamepassword.log', level=logging.INFO)
#print os.getcwd()
#sys.exit()

def main():
    try:
        fi2 = open(sys.argv[1],'r+')
        fi = fi2.readlines()
        fi2.close()

        fo = open(sys.argv[2],'w+')
        print "Init files"
        output_list=[]
        for x in xrange(len(fi)):
            mail = fi[x].replace("\n","").replace("\x00","").replace("\000","").rstrip(' \t\r\n\0').strip()
            outputss = db.creddump.find({"mail":mail})
            if outputss:
                for xx in outputss:
                    out = "%s,%s\n" % (xx['mail'],xx['pass'])
                    fo.write(out)

            #if outputss == 0:
            ##    out = mail+',N/A\n'
            #    fo.write(out)
            #else:
            #    out = mail+',Found\n'
            #    fo.write(out)

        fo.close()
        logging.info("Completed %s of query in %s seconds",len(output_list),time.time()-timer)

    except Exception,err:
        print err
        logging.info(err)



if __name__ == "__main__":
   main()
 

