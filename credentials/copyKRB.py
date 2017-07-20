osslcmd = "openssl x509 -in /tmp/x509up_u`id -u` -noout -enddate"
import subprocess
def getKerberosDate(hostname):
    osslcmd = "ssh %s klist"%hostname
    proc = subprocess.Popen(osslcmd,stdout=subprocess.PIPE,shell=True)
    (out, err) = proc.communicate()
    outwithoutreturn = out.rstrip('\n')[9:]    
    pos = outwithoutreturn.find("renew until")
    if pos>0:
        return outwithoutreturn[pos+12:pos+31]


import datetime
def ConvertDate(inp):
    return datetime.datetime.strptime(inp,"%m/%d/%Y %X")


servers = ["lhcbportal",
           "lhcbwn01",
           "lhcbwn02",
           "lhcbwn03"]

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

import sys

argv = sys.argv
if len(sys.argv) <= 1:
    argv += ["usage"] 

def show():
    for s in servers:
        print s,getKerberosDate(s)

def usage():
    print "python copy.py [show|copy|getbest|usage]"

TheDict = {"show":show,
           "getbest":getBest,
           "copy":copy,
           "usage":usage}

for cmd in argv[1:]:
    TheDict[cmd]()
