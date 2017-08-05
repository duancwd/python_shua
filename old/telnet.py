import getpass
import sys
import telnetlib
import time

HOST = "10.21.78.150"
#user = raw_input("Enter your remote account:")
#password = getpass.getpass()
user = "cisco"
password = "cisco"
tn = telnetlib.Telnet(HOST,timeout = 15)


tn.read_until("Username:")
tn.write(user.encode('ascii') + "\n\r")
#tn.write(user + "\n")
if password:
    tn.read_until("Password:")
    tn.write(password.encode('ascii') +"\n\r")
    #tn.write(password + "\n
#print tn.read_all()
tn.write("sys \n\r")

#tn.write("vlan 2 \n\r")

tn.write("display interface brief  | in GigabitEthernet0/0/11"+"\n\r")
#time.sleep(1)
#print tn.read_very_lazy()
#tn.read_until("]")
print tn.read_until("]")

tn.write("return"+"\n\r")

tn.read_until(">")

#tn.write("quit"+"\n\r")
tn.close()
print tn.read_all()
#op=tn.read_very_eager()
#op=tn.read_some()
#op=tn.read_until('#')

#op=tn.read_until("quit")
#op= tn.read_all()


