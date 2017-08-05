import serial
import io
import time


#ser = serial.Serial(2, baudrate=9600, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False)

ser = serial.Serial()
filename = "300.txt"
#q = Queue.Queue()
user  = "cisco"
password = "cisco"
enable_password = "cisco"


def serNetCall():
 ser.baudrate = 9600
 ser.port = 'COM6'
 ser.bytesize=8
 ser.stopbits=1
 ser
 ser.open()
 #ser.write(username+"\n\r")
 #ser.write(password+"\n\r")
 #ser.write("enable"+"\n\r")


def shua_file():
    count = 0
    lines = [line.rstrip('\n\r') for line in open(filename)]
    #print lines
    for line in lines:
     count=count+1;
     
     print line+"\n\r"
     time.sleep(0.5)
     if "^" not in ser.read_all(): 
      ser.write(line +'\n\r')
      print "line %(count)d writing was successful"%{"count":count}
    
     else:
      print "WTF£¬something wrong!"
      break
    ser.write("commit"+"\n\r") 
    ser.close()
    

#if __name__=='__main__':
serNetCall()
time.sleep(5)
ser.write("root"+"\n\r")
ser.write("p@ssw0rd"+"\n\r")
ser.write("cli"+"\n\r")
ser.write("configure"+"\n\r")
    #if "root@CSR-ALIPAY-1.OE24" not in ser.read_all():
    # ser.close()
    #else:
shua_file()
    
