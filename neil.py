#
# serialstep.2.py
#    serial step-and-direction, 2 port
#
# Neil Gershenfeld  5/25/21
# This work may be reproduced, modified, distributed,
# performed, and displayed for any purpose, but must
# acknowledge this project. Copyright is retained and
# must be preserved. The work is provided as is; no
# warranty is provided, and users accept all liability.
#
import serial,sys,time,signal
if (len(sys.argv) != 5):
   print("command line: serialstep.2.py port0 port1 speed delay")
   sys.exit()
device0 = sys.argv[1]
device1 = sys.argv[2]
baud = int(sys.argv[3])
delay = float(sys.argv[4])
print('open '+device0+' at '+str(baud)+' delay '+str(delay))
port0 = serial.Serial(device0,baudrate=baud,timeout=0)
print('open '+device1+' at '+str(baud)+' delay '+str(delay))
port1 = serial.Serial(device1,baudrate=baud,timeout=0)
count = 0;
maxcount = 5000;
forward = b'b'
reverse = b't'
#
# alarm handler
#
def handler(signum,stack):
   global count
   count += 1
   if (count < maxcount/4):
      if (count%4 == 0):
         port0.write(forward);
   elif (count < maxcount/2):
      if (count%3 == 0):
         port1.write(forward);
   elif (count < 3*maxcount/4):
      if (count%2 == 0):
         port0.write(forward);
         port1.write(reverse);
   elif (count < maxcount):
      port0.write(reverse);
      port1.write(forward);
   else:
      count = 0
#
# start alarm
#
signal.signal(signal.SIGALRM,handler)
signal.setitimer(signal.ITIMER_REAL,1,delay)
#
# do nothing
#
while (1):
   0  
