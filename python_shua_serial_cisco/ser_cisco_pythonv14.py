import serial
import io
import time
#############################
ser = serial.Serial()       
filename = "abcd.log"                   
user  = "cisco"
password = "eccom@123"
enable_password = ""
console ="COM8"
baudrate = 9600
stopbits = 1
bytesize = 8
#############################
def serNetCall():
 ser.baudrate = baudrate
 ser.port = console
 ser.bytesize= bytesize
 ser.stopbits=stopbits
 ser
 ser.open()
 time.sleep(5)
 ser.write('  \n\r')
 if not ser.isOpen():
     print"please check console informtion"
 print"connection successful"

def login():
 print "loging in"
 ser.write(" \n\r")
 ser.write("exit \n\r")
 ser.write("exit \n\r")
 ser.write(" \n\r")
 time.sleep(5)
 input_data = ser.read(ser.inWaiting())
 print input_data
 if 'Username' in input_data:
  ser.write(user + '\r\n')
 #ser.write("    "+"\n\r")
 time.sleep(1)
 input_data = ser.read(ser.inWaiting())
 if 'Password' in input_data:
  ser.write(password+"\n\r")

 ser.write("enable"+"\n\r")
 ser.write(enable_password+"\n\r")
 ser.write("conf t"+"\n\r")
 print"login successful"
 


def shua_file():
    count = -1
    lines = [line.rstrip('\n\r') for line in open(filename)]
    #print lines
    ser.write('    \n\r')
    print ser.read(ser.inWaiting())
    ser.write('\n\r')
    print ser.read(ser.inWaiting())
    ser.write('\n\r')
    print ser.read_all()
    for line in lines:
     #print line+"\n\r"
     time.sleep(0.2)

     if "^" not in ser.read(ser.inWaiting()):
      ser.write(line +'\n\r')
      print "line %(count)d writing was successful"%{"count":count}
      count=count+1
      print line
      print ser.read(ser.inWaiting())
     else:
      print ser.read(ser.inWaiting())
      print "WTF£¬something wrong!"
      break
    ser.close()
    print"[####################] 100% -- SUCCESS"


if __name__=='__main__':
    serNetCall()
    login()
    shua_file()
    
