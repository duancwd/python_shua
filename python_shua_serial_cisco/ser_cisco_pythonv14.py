import serial
import io
import time

ser = serial.Serial()
filename = "300.log"
#q = Queue.Queue()
user  = "cisco"
password = "cisco"
enable_password = ""
console ="COM6"

def serNetCall():
 ser.baudrate = 9600
 ser.port = console
 ser.bytesize=8
 ser.stopbits=2
 ser
 ser.open
 #ser.write(username+"\n\r")
 #ser.write(password+"\n\r")
 ser.write("enable"+"\n\r")
 ser.write(enable_password+"\n\r")


 def shua_file():
    count = 0
    lines = [line.rstrip('\n\r') for line in open(filename)]
    #print lines
    for line in lines:
     count=count+1;
     
     #print line+"\n\r"
     time.sleep(1)
     if "^" not in ser.read_all(): 
      ser.write(line +'\n\r')
      print "line %(count)d writing was successful"%{"count":count}
      print read(10)
     else:
      print "WTF£¬something wrong!"
      break
    ser.close()


if __name__=='__main__':
    serNetCall()
    ser.write("conf t"+"\n\r")
    shua_file()
    
