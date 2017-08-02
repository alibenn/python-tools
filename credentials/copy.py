osslcmd = "openssl x509 -in /tmp/x509up_u`id -u` -noout -enddate"
import subprocess
def getGridProxyExpiryDate(hostname):
    osslcmd = "ssh %s openssl x509 -in /tmp/x509up_u`id -u` -noout -enddate"%hostname
    proc = subprocess.Popen(osslcmd,stdout=subprocess.PIPE,shell=True)
    (out, err) = proc.communicate()
    outwithoutreturn = out.rstrip('\n')[9:]    
    return outwithoutreturn

import datetime
def ConvertDate(inp):
    return datetime.datetime.strptime(inp,"%b %d %X %Y %Z")

from servers import servers

def getBest():
    ts = {}
    for s in servers:
        t = getGridProxyExpiryDate(s)
        if t:
           ts[ConvertDate(t)] = s
    besthost = ts[max(ts.keys())]
    print "getting proxy from", besthost
    proc = subprocess.Popen("scp %s:/tmp/x509up_u`id -u` /tmp/x509up_u`id -u`"%besthost,shell=True)
    (out, err) = proc.communicate()

def copy():
    for s in servers:
        proc = subprocess.Popen("scp /tmp/x509up_u`id -u` %s:/tmp/x509up_u`id -u`"%s,shell=True)
        (out, err) = proc.communicate()

import sys

argv = sys.argv
if len(sys.argv) <= 1:
    argv += ["usage"] 

def show():
    for s in servers:
        print s,getGridProxyExpiryDate(s)

def usage():
    print "python copy.py [show|copy|getbest|usage]"

TheDict = {"show":show,
           "getbest":getBest,
           "copy":copy,
           "usage":usage}

for cmd in argv[1:]:
    TheDict[cmd]()
