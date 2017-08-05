import getpass 
import sys 
import telnetlib 

HOST = '10.21.78.150' 
user = "cisco"
password = "cisco"
tn = telnetlib.Telnet(HOST, timeout = 20) 
tn.read_until("Username: ") 
tn.write(user + '\n\r')
#tn.write(user.encode('ascii') + "\n\r")

if password:
    tn.read_until('Password:')
    #tn.write(password.encode('ascii') +"\n\r")
    tn.write(password + '\n\r') 
tn.write('enable \n\r') # go to exec mode 
#tn.read_until('Password: ') #prompt to go to exec mode 
tn.write("cisco"+'\n\r')
tn.write("conf t"+'\n\r') 
tn.write("inter loop 0"+'\n\r')
tn.write("ip add 10.1.1.1 255.255.255.0"+'\n\r') 
 
#tn.write('do sh int status' '\n\r') #run this command, read this from file when i figure out how 


tn.write('end' '\n\r') 

print tn.read_all() 

tn.close() 
