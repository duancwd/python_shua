# -*- coding: cp936 -*-
import os
import telnetlib
import time
from multiprocessing import Process
import Queue
import threading
import os

#----------------------------------
host  = "192.168.1.2"
user  = "cisco"
password = "cisco"
enable_password = "cisco"
filename = "192.168.1.2.log"
#------------------------------------


telnet  = telnetlib.Telnet(host,timeout= 3600) 

q = Queue.Queue()

def telNetCall():
 
 telnet.read_until('Username: ', 3)
 telnet.write(user + '\r')
 telnet.read_until('Password: ', 3)
 telnet.write(password + '\r')
 telnet.write('enable' + '\r\n')
 telnet.write(enable_password + '\r\n')
 




def show_version():
 telNetCall()
 telnet.write('term len 0' + '\r\n')
 telnet.write("show version"+ "\r\n")
 telnet.write("\r\n")
 #telnet.write(string)
 telnet.write("show run"+ "\r\n")
 telnet.write('exit' + '\r')
 a=telnet.read_all()
 print a
 f = open(host+'.log', 'w')
 f.write(str(a))


def shua_file():
    count = 0
    lines = [line.rstrip('\n\r') for line in open(filename)]
   # print lines
    for line in lines:
     count=count+1;
     q.put(count)
     #print line+"\n\r"
     time.sleep(0.4)
     if q.get()< 9999:
      telnet.write(line +'\n\r')
      print "line %(count)d writing was successful"%{"count":count}
     else:
      print "WTF，something wrong here!"
      break
    telnet.close


#show_version()
def pro2():
    print telnet.read_until("^"or "% Invalid input detected at '^' marker.")
    q.put(9999)
    telnet.close
if __name__=='__main__':
 telNetCall()
 telnet.write("conf t \n\r")
 p1 = threading.Thread(target=shua_file, args=())
 p2 = threading.Thread(target=pro2, args=())
 p1.start()
 p2.start()
 #p1.stop()
 #p2.stop()
    

