#!/usr/bin/env python

import argparse
import netsnmp
import sys

# Arguments

arg = argparse.ArgumentParser(description='This plugin checks current connections to VIP for Cisco ACE4710.')

arg.add_argument('-H', type=str, dest='vhost', help='host')
arg.add_argument('-n', type=str, dest='vcomm', help='community')
arg.add_argument('-f', type=str, dest='vfarm', help='classname_vip')
arg.add_argument('-w', type=int, dest='vwarn', help='warning')
arg.add_argument('-c', type=int, dest='vcrit', help='critical')

res = arg.parse_args()

# Var
host = res.vhost
comm = res.vcomm
farm = res.vfarm
oidname = netsnmp.Varbind('.1.3.6.1.4.1.9.9.161.1.4.2.1.2.1')
oidcount = netsnmp.Varbind('.1.3.6.1.4.1.9.9.161.1.4.2.1.6')
min = 0
max = 100000
war = res.vwarn
crit = res.vcrit

# Get counters
farmlist = netsnmp.snmpwalk(oidname, Version=2, DestHost=host, Community=comm)
countlist = netsnmp.snmpwalk(oidcount, Version=2, DestHost=host, Community=comm)

# Make dictionary
dictlist = dict(zip(farmlist, countlist))
farmvar = dictlist.get(farm)
intfarmvar = int(farmvar)

# Print var
firstpart = farmvar + ' |'
secondpart = ' current_connects=' + farmvar + ';' + str(warn) + ';' + str(crit)

# Check conditions
if ((intfarmvar >= min) and (intfarmvar <= max)):
    if intfarmvar <= warn:
        print "Ok - " + firstpart + secondpart
        sys.exit(0)
    elif intfarmvar <= crit:
        print "Warning - " + firstpart + secondpart
        sys.exit(1)
    else:
        print "Critical - " + firstpart + secondpart
        sys.exit(2)
else:
    print "Unknown - Check hostname or community. Reason: unknown"
    sys.exit(3)
