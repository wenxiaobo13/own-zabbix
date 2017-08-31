#!/usr/bin/python

#################################################################
#
# zabbix-docker-discover.py
#
#   A program that produces LLD information for Zabbix to
#   process Docker instances.
#
# Version: 1.0
#
# Author: Richard Sedlak
#
#################################################################

import subprocess
import commands
import json
import time
strings = subprocess.Popen("sudo docker ps -a", shell=True, stdout=subprocess.PIPE).stdout.readlines()

l=list()
for i in range(1,len(strings)):
        pstring = strings[i].split()
#       zd_name = subprocess.call("docker inspect pstring[1] | grep MESOS_TASK_ID | sed -n '2p' |cut -d : -f 2 | cut -d \" -f 2 | cut -d . -f 1" , shell=True)
        cmd = "sudo docker inspect " + pstring[0] + "|"+" grep MESOS_TASK_ID" + "|" + "grep -v =" "|" + "cut -d : -f 2"
        (status,inspectoutput) = commands.getstatusoutput(cmd)
        zd_split = inspectoutput.strip(' ').strip('"').strip(',').strip('"')
        d=dict()
        if zd_split.strip()=='':
                d["{#ZD_ID}"]=pstring[-1]
                d["{#ZD_IMAGE}"]=pstring[1]
                d["{#ZD_NAME}"]=pstring[-1]
        else:
                d["{#ZD_ID}"]=pstring[-1]
                d["{#ZD_IMAGE}"]=pstring[1]
                d["{#ZD_NAME}"]=zd_split

        l.append(d)

s_json=dict()
s_json["data"]=l
print json.dumps(s_json)
