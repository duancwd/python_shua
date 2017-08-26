from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('pub'),
    cmdgen.UdpTransportTarget(('192.168.1.2', 161)),'10.48.91.71 1.3.6.1.4.1.9.9.109.1.1.1.1.5')

print('\n'.join([ '%s = %s' % varBind for varBind in varBinds]))
