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

con = psycopg2.connect("host='localhost' dbname='cred_dump' user='db_user' password='password'")   
cur = con.cursor()

def main():
    try:
        fi2 = open(sys.argv[1],'r+')
        fi = fi2.readlines()
        fi2.close()

        fo = open(sys.argv[2],'w+')
        print "Init files"
        output_list=[]
        for x in xrange(len(fi)):
            #print fi[x]
            outputss = QueryCredDB(fi[x].replace("\n","").replace("\x00","").replace("\000","").rstrip(' \t\r\n\0').strip())
            output_list.append(outputss)
            #print "here 2 %s" % (outputss)
            if len(outputss[0]) == 2:
                out = outputss[0][0]+','+outputss[0][1]+'\n'
                fo.write(out)
                #print "Added %s" % (out)

        fo.close()
        logging.info("Completed %s of query",len(output_list))

    except Exception,err:
        print err
        logging.info(err)
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)


def QueryCredDB(data):
    try:
        timer = time.time()
        #con = psycopg2.connect("host='localhost' dbname='cred_dump' user='db_user' password='password'")   
        #cur = con.cursor()
        sql = "SELECT COUNT(EMAIL) FROM BREACHDUMPS where EMAIL = '%s'" % (data.replace('"', '').replace("'", ""))
        cur.execute(sql)
        row = cur.fetchone()
        row = int(row[0])

        #print "Time to Query1 to DB %s %s %s\n" % (time.time()-timer,data,row)
        if row == 0:
            return_output = []
            return_output.append([data,"N/A"])
            return return_output
        else:
            return_output = []
            return_output.append([data,"Found"])
            return return_output
        
        #print "Time to Query2 to DB %s %s\n" % (time.time()-timer,data)
        
        if con:
            con.close()

          #break

    except psycopg2.DatabaseError, e:
        if con:
            try:
                con.rollback()
            except:
                pass
                
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        logging.info('Postgresql Error with file %s - %s',data,e)
        print 'Postgresql Error with file %s - %s' % (data,e)
        #problematic=1
        time.sleep(5)

    except Exception,err:
        logging.info("Unknown Error %s %s",err,data)
        print err
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)

if __name__ == "__main__":
   main()

