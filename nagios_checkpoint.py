#!/usr/bin/env python

import argparse
import netsnmp
import sys


# Print var
def cycle_count(text, variable, min, max, warn, critic):
    firstpart = variable + ' |'
    secondpart = text + variable + ';' + str(warn) + ';' + str(critic)
    ivar = int(variable)
    # Check conditions
    if ((ivar >= min) and (ivar <= max)):
        if ivar <= warn:
            print "Ok - " + firstpart + secondpart
            sys.exit(0)
        else:
            if ivar < critic:
                print "Warning - " + firstpart + secondpart
                sys.exit(1)
            else:
                print "Critical - " + firstpart + secondpart
                sys.exit(2)
    else:
        print "Unknown - Check hostname or community. Reason: unknown"
        sys.exit(3)


def cycle_temp_count(text, tn1, tn2, tc1, tc2, imin, imax, warn, critic):
    firstpart = tn1 + '=' + tc1 + 'C ' + tn2 + '=' + tc2 + 'C |'
    secondpart = text + tn1 + '=' + tc1 + 'C ' + ';' + tn2 + '=' + tc2 + ';'
    thirdpart = str(warn) + ';' + str(critic)
    ivar1 = int(float(tc1))
    ivar2 = int(float(tc2))
    # Check conditions
    if ((ivar1 >= imin) and (ivar1 <= imax)) and ((ivar2 >= imin) and (ivar2 <= imax)):
        if ((ivar2 <= warn) and (ivar2 <= warn)):
            print "Ok - " + firstpart + secondpart + thirdpart
            sys.exit(0)
        else:
            if ((ivar1 < critic) or (ivar2 < critic)):
                print "Warning - " + firstpart + secondpart + thirdpart
                sys.exit(1)
            else:
                print "Critical - " + firstpart + secondpart + thirdpart
                sys.exit(2)
    else:
        print "Unknown - Check hostname or community. Reason: unknown"
        sys.exit(3)


def cycle_status():
    if ivar == 0:
        print "Ok - " + firstpart + secondpart
        sys.exit(0)
    else:
        print "Critical - " + firstpart + secondpart
        sys.exit(2)


# Functions
def cpu_load_av(vhost, vcomm, vwar, vcrit):
    oid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.2.4')
    count = netsnmp.snmpwalk(oid, Version=2, DestHost=vhost, Community=vcomm)
    cpuresult = count[0]
    cputext = ' CPU load average='
    cpumin = 0
    cpumax = 100
    cpuwar = vwar
    cpucrit = vcrit
    cycle_count(cputext, cpuresult, cpumin, cpumax, cpuwar, cpucrit)


def core1_load_av(vhost, vcomm, vwar, vcrit):
    oid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.5.1.5.1')
    count = netsnmp.snmpwalk(oid, Version=2, DestHost=vhost, Community=vcomm)
    coreresult = count[0]
    coretext = ' Core1 load average='
    coremin = 0
    coremax = 100
    corewar = vwar
    corecrit = vcrit
    cycle_count(coretext, coreresult, coremin, coremax, corewar, corecrit)


def core2_load_av(vhost, vcomm, vwar, vcrit):
    oid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.5.1.5.2')
    count = netsnmp.snmpwalk(oid, Version=2, DestHost=vhost, Community=vcomm)
    coreresult = count[0]
    coretext = ' Core2 load average='
    coremin = 0
    coremax = 100
    corewar = vwar
    corecrit = vcrit
    cycle_count(coretext, coreresult, coremin, coremax, corewar, corecrit)


def freeram_func(vhost, vcomm, vwar, vcrit):
    oid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.4.4')
    count = netsnmp.snmpwalk(oid, Version=2, DestHost=vhost, Community=vcomm)
    framresult = count[0]
    framtext = ' FreeRAM='
    frammin = 0
    frammax = 5000000000
    framwar = vwar
    framcrit = vcrit
    cycle_count(framtext, framresult, frammin, frammax, framwar, framcrit)


def temp_func(vhost, vcomm, vwar, vcrit):
    tnoid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.8.1.1.2')
    tvoid = netsnmp.Varbind('.1.3.6.1.4.1.2620.1.6.7.8.1.1.3')
    tname = netsnmp.snmpwalk(tnoid, Version=2, DestHost=vhost, Community=vcomm)
    tcount = netsnmp.snmpwalk(tvoid, Version=2, DestHost=vhost, Community=vcomm)
    tn1 = tname[0]
    tn2 = tname[1]
    tc1 = tcount[0]
    tc2 = tcount[1]
    ttext = 'Temperature='
    tmin = 0
    tmax = 1000
    twar = vwar
    tcrit = vcrit
    cycle_temp_count(ttext, tn1, tn2, tc1, tc2, tmin, tmax, twar, tcrit)


# Arguments
parser = argparse.ArgumentParser(description='This plugin checks multiple parameters of Checkpoint FW.')

parser.add_argument('-H', type=str, dest='host', help='hostname')
parser.add_argument('-n', type=str, dest='comm', help='community')
parser.add_argument('-t', type=str, dest='type', help='type')
parser.add_argument('-o', type=str, dest='opt', help='options')
parser.add_argument('-w', type=int, dest='war', help='warning')
parser.add_argument('-c', type=int, dest='crit', help='critical')

res = parser.parse_args()
vhost = res.host
vcomm = res.comm
vtype = res.type
vopt = res.opt
vwar = res.war
vcrit = res.crit


def count_func():
    if vopt == 'cpu':
        cpu_load_av(vhost, vcomm, vwar, vcrit)
    elif vopt == 'core1':
        core1_load_av(vhost, vcomm, vwar, vcrit)
    else:
        if vopt == 'core2':
            core2_load_av(vhost, vcomm, vwar, vcrit)
        elif vopt == 'fram':
            freeram_func(vhost, vcomm, vwar, vcrit)
        else:
            if vopt == 'temp':
                temp_func(vhost, vcomm, vwar, vcrit)
            else:
                print('There is error, check options.')


def status_func():
    if vopt == 'fan':
        fan_status(vhost, vcomm)
    elif vopt == 'power':
        power_status(vhost, vcomm)
    else:
        print('Value opt must be either fan or power!')
        sys.exit(0)


if vtype == 'counter':
    count_func()
elif vtype == 'status':
    status_func()
else:
    print('Value of type must be either counter or status!')
    sys.exit(0)
