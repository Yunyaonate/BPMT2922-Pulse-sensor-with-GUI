##
## Read from a serial port and print received data.
## Set portName to be the name of teh serial port to be used.
##
## Author:  Greg Watkins
## Date:    10 Sep 2021
##

import serial
import time
import sys

serialString = ""  # Used to hold data coming over UART
# portName = "COM6"          # PC format
#portName = "/dev/tty..."    # Mac format
portName = "/dev/tty.ESP32testG01-ESP32SPP"    # Mac format

import time
from classDefine import data
from classDefine import alarm
from classDefine import print_message
from alarmFunction import commsAlarm
from alarmFunction import bpmAlarm
from dataProcessing import fourBytesToNum
from dataProcessing import meanBpm


# define the serial port.
# specify parameters as needed
serialPort = serial.Serial()
serialPort.port=portName 
serialPort.baudrate=115200
serialPort.bytesize=8
serialPort.timeout=2 
serialPort.stopbits=serial.STOPBITS_ONE

# open the port
try:
    serialPort.open()
except:
    print("Port open failed: " + portName)
    for e in sys.exc_info():
        print("  ",e)
    
lastMessage = time.time();
if serialPort.isOpen():
    print("**************************************")
    print("** Serial port opened: {}".format(portName))
    print("**************************************")

    while 1:
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            print(serialString)

            this_message = serialString
            data.raw.append(this_message)

            dataType = int(this_message[2])
            fourBytesToNum(dataType,this_message)



            #print(serialString.decode("Ascii"), end = "")
            lastMessage = time.time()

        # Should receive 2 messages / s, if less than this, reestablish comms
        if (time.time() - lastMessage) > 2.0:

            serialPort.close()
            print("**************************************")
            print("** Serial port closed: {}".format(portName))
            print("**************************************")

            time.sleep(0.5)

            for i in range(10):
                try:
                    print("Trying to reconnect...")
                    serialPort.open()
                    if serialPort.isOpen:
                        print("Connected")
                        this_message = serialString
                        data.raw.append(this_message)

                        dataType = int(this_message[2])
                        fourBytesToNum(dataType,this_message)



                        ## Try everything here:

                    time.sleep(2)

                except:
                    print("Port open failed: " + portName)
                    
else:
    print("Exiting")
    for e in sys.exc_info():
        print("  ",e)
