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
logging.basicConfig(filename='pg_insert.log', level=logging.INFO)
#print os.getcwd()
#sys.exit()


def chunk(xs, n):
    '''Split the list, xs, into n chunks'''
    L = len(xs)
    assert 0 < n <= L
    s = L//n
    return [xs[p:p+s] for p in range(0, L, s)]


for root,directory, filenames in os.walk(sys.argv[1]):
    lines = ""
    for file in filenames:         
        pathss = os.path.join(root,file)
        #print root+"/"+sys.argv[2]
        #continue
        if ((os.path.isfile(pathss)) and (pathss == root+"/"+sys.argv[2]) or (os.path.isfile(pathss)) and (sys.argv[2] == "all")):
            filecounter +=1
            print "\nParsing %s" % (pathss)
            con = None
            with open(pathss) as line:
                timer = time.time()
                credential_holder = []
                for lines in line:
                    try:    
                        if ("@" in lines) and (":" in lines):
                            #lines = unicode(lines, "utf-8")
                            lines = lines.decode('utf8').encode('ascii', errors='ignore')
                            if  "@" in lines.split(':')[-2]:
                                mail =lines.split(':')[0]
                                password =lines.split(':')[1]
                                if "@" not in mail:
                                    mail =lines.split(':')[1]
                                    password =lines.split(':')[2]
                                elif "@" not in mail:
                                    mail =lines.split(':')[2]
                                    password =lines.split(':')[3]
                                elif "@" not in mail:
                                    raise Exception

                                mail = mail.replace("\n","").replace("\x00","").replace("\000","").rstrip(' \t\r\n\0').strip()
                                password = password.replace("\n","").replace("\x00","").replace("\000","").rstrip(' \t\r\n\0').strip()

                                #password = password[:3]+"*********"
                                if "pastebin.com/u" in password:
                                    password = "*********"
                                elif password in stupid_pass:
                                    password = "*********"

                                if (len(mail)<254) and (len(password)<254):
                                    if (mail != None) and (len(mail) > 5):
                                        credential_holder.append((mail,password))
                                else:
                                    print "Length Error %s %s" % (mail,password)
                                    logging.info('Length Error %s - %s',mail,password)
                   

                    except IndexError:
                        pass

                    except UnicodeDecodeError:
                        pass

                    except Exception,err:
                        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                        print "%s - %s" % (err,lines)

                problematic=0
                #while(1):
                try:
                    con = psycopg2.connect("host='localhost' dbname='cred_dump' user='db_user' password='password'")   
                    cur = con.cursor()
                    print "Time to parse %s" % (time.time()-timer)
                    timer = time.time()
                    print "Inserting %s record into DB for %s" % (len(credential_holder),pathss)
                    if (len(credential_holder) > 50000000) or (problematic==1):
                        for d in xrange(len(credential_holder)):
                            cur.execute("INSERT into breachdumps(EMAIL, PASS) VALUES (%s, %s)", credential_holder[d])
                        print "Time to formulate Slow SQL %s" % (time.time()-timer)
                        timer = time.time()  
                        con.commit()
                    elif (len(credential_holder) > 2000000) and (problematic==0):
                        chunking = []
                        chunking = chunk(credential_holder,10)
                        for xxx in xrange(len(chunking)):
                            dataText = ','.join(cur.mogrify('(%s,%s)', row) for row in chunking[xxx])
                            cur.execute('insert into breachdumps(EMAIL, PASS) values ' + dataText)
                            print "Time to formulate Fast SQL %s" % (time.time()-timer)
                            timer = time.time()
                            con.commit()
                    else:
                        dataText = ','.join(cur.mogrify('(%s,%s)', row) for row in credential_holder)
                        cur.execute('insert into breachdumps(EMAIL, PASS) values ' + dataText)
                        print "Time to formulate Fast SQL %s" % (time.time()-timer)
                        timer = time.time()
                        con.commit()
                    print "Time to Insert to DB %s\n" % (time.time()-timer)

                    if con:
                        con.close()
                    #break

                except psycopg2.DatabaseError, e:
                    if con:
                        try:
                            con.rollback()
                        except:
                            pass

                    logging.info('Postgresql Error with file %s - %s',pathss,e)
                    print 'Postgresql Error with file %s - %s' % (pathss,e)
                    #problematic=1
                    time.sleep(5)

                except Exception,err:
                    logging.info("Unknown Error %s",err)
                    print err



print "\n**************\n %s of files parsed\n Elapsed time: %s **************\n" % (filecounter,str(datetime.timedelta(seconds=time.time()-timer)))

