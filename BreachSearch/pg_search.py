###
# Name:    DumpMyCred
# Description: Credential Dump Parser script
# Author:      SAINTz
# Version:     0.1 - 12 December 2017
# License:     GNU/GPL
##

#import pymongo
import os
import sys
import datetime
import time
import psycopg2
import logging

timer = time.time()
#client = pymongo.MongoClient("localhost", 27017)
#db=client.credd
filecounter=0

stupid_pass= ["gayASSfagpastebinleaks","plaintext_password",""]
stupid_pass_keyword = ['pastebin.com/u']
logging.basicConfig(format='%(asctime)s - %(message)s',filename='pg_search.log', level=logging.INFO)
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
            outputss = QueryCredDB(fi[x])
            output_list.append(outputss)
            if len(outputss) > 2:
                out = outputss[0]+','+outputss[1]
                fo.write(out)

        fo.close()
        logging.info("Completed %s of query",len(output_list))

    except Exception,err:
        print err
        logging.info(err)


def QueryCredDB(data):
    try:
        timer = time.time()
        con = psycopg2.connect("host='localhost' dbname='cred_dump' user='db_user' password='password'")   
        cur = con.cursor()
        cur.execute("SELECT COUNT(EMAIL) FROM BREACHDUMPS where EMAIL like '%data%'")
        row = cur.fetchone()
        if row == None:
            return_output = []
            return_output.append([data,"N/A"])
            return return_output
        else:
            return_output = []
            return_output.append([data,"Found"])
            return return_output

        print "Time to Query to DB %s %s\n" % (time.time()-timer,data)

        if con:
            con.close()
        #break

    except psycopg2.DatabaseError, e:
        if con:
            try:
                con.rollback()
            except:
                pass

        logging.info('Postgresql Error with file %s - %s',data,e)
        print 'Postgresql Error with file %s - %s' % (data,e)
        #problematic=1
        time.sleep(5)

    except Exception,err:
        logging.info("Unknown Error %s %s",err,data)
        print err

if __name__ == "__main__":
   main()


