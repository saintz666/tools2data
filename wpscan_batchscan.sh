#!/bin/bash
# Author : SAINTz
# Twitter: @__SAINTz__

domains='www.example1.com www.example2.com www.example3.com'

destination=/data/
for n in $domains; do

    echo -e "\nScanning $n ... "
    wpscan --url $n --batch --no-color > $destination/$n.wpscan.log

done
