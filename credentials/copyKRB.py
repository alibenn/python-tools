import subprocess
def getKerberosDate(hostname):
    osslcmd = "ssh %s klist"%hostname
    proc = subprocess.Popen(osslcmd,stdout=subprocess.PIPE,shell=True)
    (out, err) = proc.communicate()
    for l in out.split("\n"):
        l = l.replace("201","1") ## 2017 -> 17 ... 
        if "afs/cern.ch@CERN.CH" in l:
            return l[19:36]
#    outwithoutreturn = out.rstrip('\n')[9:]    
#    print out ## debug
#    pos = outwithoutreturn.find("renew until")
#    if pos>0:
#        return outwithoutreturn[pos+12:pos+31]


import datetime
def ConvertDate(inp):
    return datetime.datetime.strptime(inp,"%m/%d/%y %X")

from servers import servers

def getBest():
    ts = {}
    for s in servers:
        t = getKerberosDate(s)
        if t:
           ts[ConvertDate(t)] = s
    besthost = ts[max(ts.keys())]
    print "getting token from", besthost
    proc = subprocess.Popen("scp %s:/tmp/krb5cc_`id -u` /tmp/krb5cc_`id -u`"%besthost,shell=True)
    (out, err) = proc.communicate()

def copy():
    for s in servers:
        proc = subprocess.Popen("scp /tmp/krb5cc_`id -u` %s:/tmp/krb5cc_`id -u`"%s,shell=True)
        (out, err) = proc.communicate()


def renew():
    for s in servers:
        proc = subprocess.Popen("ssh %s kinit -R"%s,shell=True)
        (out, err) = proc.communicate()

def aklog():
    for s in servers:
        proc = subprocess.Popen("ssh %s aklog"%s,shell=True)
        (out, err) = proc.communicate()

import sys

argv = sys.argv
if len(sys.argv) <= 1:
    argv += ["usage"] 

def show():
    for s in servers:
        print s,getKerberosDate(s)

def usage():
    print "python copy.py [show|copy|getbest|usage|renew|aklog]"

TheDict = {"show":show,
           "getbest":getBest,
           "copy":copy,
           "usage":usage,
           "renew":renew,
           "aklog":aklog}

for cmd in argv[1:]:
    TheDict[cmd]()
