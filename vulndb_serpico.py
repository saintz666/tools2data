###
# Name:    VulnDB_Json_serpico
# Description: Script to Parse VulnDB to Serpico Vulnerability Findings
# Author:      SAINTz
# Twitter: @__SAINTz__
# Version:     0.1 - 17 August 2018
# License:     GNU/GPL
##

import json
from vulndb import DBVuln

DB_IDs = DBVuln.get_all_db_ids()

export_json = []
for x in DB_IDs:
	dbv = DBVuln.from_id(x)
	data_tmp = {"affected_hosts": "null","affected_users": 10,"approved": "true","damage": 10,"discoverability": 10,"dread_total": 0,"effort": "Planned","exploitability": 10,"id": dbv.id,"overview": "<paragraph>"+dbv.description +"</paragraph>","poc": "<paragraph></paragraph>","references": dbv.references,"remediation": "<paragraph>"+dbv.fix_guidance+"</paragraph>","reproducability": 10,"risk": dbv.severity,"title": dbv.title,"type": "null"}
	export_json.append(data_tmp)

with open('findings_vulndb.json', 'w') as outfile:
    json.dump(export_json, outfile)


