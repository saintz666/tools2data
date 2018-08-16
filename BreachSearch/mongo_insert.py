###
# Name:    DumpMyCred
# Description: Credential Dump Parser script
# Author:      SAINTz
# Twitter: @__SAINTz__
# Version:     0.1 - 12 December 2017
# License:     GNU/GPL
##

#import pymongo
import os
import sys
import datetime
import time
import pymongo
import logging

timer = time.time()
client = pymongo.MongoClient("localhost", 27017)
db=client.credd
filecounter=0
timer = time.time()
stupid_pass= ["gayASSfagpastebinleaks","plaintext_password",""]
stupid_pass_keyword = ['pastebin.com/u']
logging.basicConfig(filename='mongo_insert.log', level=logging.INFO)
#print os.getcwd()
#sys.exit()
pathss = sys.argv[1]
print "\nParsing %s" % (pathss)
con = None

try:
    with open(pathss) as line:
        print "Time to load file %s\n" % (time.time()-timer)
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
                                db.creddump.insert({"mail":mail,"pass":password})
                                #credential_holder.append((mail,password))
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

except Exception,err:
    logging.info(err)

print "\n**************\n %s of files parsed\n Elapsed time: %s **************\n" % (filecounter,str(datetime.timedelta(seconds=time.time()-timer)))

