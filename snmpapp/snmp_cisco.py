import os, sys
import socket
import random
from struct import pack, unpack
from datetime import datetime as dt

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString

ip='192.168.1.2'
community='pub'
value=('1.3.6.1.2.1.1.3.0')


generator = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
transport = cmdgen.UdpTransportTarget((ip, 161))

real_fun = getattr(generator, 'nextCmd')
res = (errorIndication, errorStatus, errorIndex, varBinds)\
    = real_fun(comm_data, transport, value)

if not errorIndication is None  or errorStatus is True:
       print "Error: %s %s %s %s" % res
else:
       print "%s" % varBinds
