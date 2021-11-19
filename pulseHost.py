"""
Main test file for the Host system

Author: Yunyao Duan and Jacinta Cleary, referred the sample code Greg Watkins created
Date:   11-11-2021
"""

import serial
import time
import sys

if len(sys.argv) == 2:
    portName = sys.argv[1]
else:
    portName = "COM6"          # PC format

serialString = ""  # Used to hold data coming over UART

# Define port names
# portName = "COM6"          # PC format
# portName = "/dev/tty.ESP32testG01-ESP32SPP"    # Mac format


# import classes and functions created in other files
from classDefine import data
from classDefine import alarm

from dataProcessing import fourBytesToNum
from dataProcessing import meanBpm

import guiFunctions as gui
import alarmFunction as alrm


#************************ Initialise GUI window ***************************#
# Draw GUI window
window = gui.draw_GUI_window()

# Add figures to canvas
ax1, fig1 = gui.addFigure(window["__CANVAS1__"])
ax2, fig2 = gui.addFigure(window["__CANVAS2__"])

# Define the serial port.
# Specify parameters as needed
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
    
lastMessage = time.time()

if serialPort.isOpen():
    print("**************************************")
    print("** Serial port opened: {}".format(portName))
    print("**************************************")

    bpmCnt = 0
    loopNum = 0
    startTime   = time.time()
    alarm.last_bpm_time = time.time()
     
    this_message = []

    while 1:
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            print(serialString)

            this_message = serialString
            data.raw.append(this_message)

            ##************************ Start Main Loop Here *****************************

            timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            print("\nLoop Number: ",loopNum)
            # this_message = data.raw[loopNum]

            # Initialise the old sequence nubmer, to make sure the first received sequence nubmer is always correct
            if loopNum == 0:
                data.oldSeqNum = this_message[1] - 1

            # If there's a message, do something
            if this_message == []:
                print("No message received")
            
            # Check for the COMMs Error, if there's comms error, report it, else, the input message validation pass
            elif alrm.commsAlarm(this_message) == True:
                print("{} : {}".format(timestamp,alarm.alarm_string))

            else:
                print("Input Message validation: Pass")

                # ********************** Store the pulse data (transfer the "4-digit-char" into a single number) ************
                dataType = int(this_message[2])
                fourBytesToNum(dataType,this_message)

                if dataType == ord('B'):
                    # Mark the bpm received time
                    alarm.last_bpm_time = time.time()
                    # print("bpm received time (in epoch): %.2f" %alarm.last_bpm_time)
                    
                    # Calculate mean BPM over last 15 seconds
                    bpmCnt = meanBpm(bpmCnt)
                    if alrm.bpmAlarm(data.this_bpm) == True:
                        print("{} : {}".format(timestamp,alarm.alarm_string))

            # ******************* Till now, the data is ready to be printed ****************************
            # Initialise the data to draw
            t_w_draw, pulse_draw, t_b_draw, bpm_draw = gui.get_data_to_draw()

            # Now do GUI actions (update animated plot, bpm alarm, current and mean bpm, and response to the user's action)
            if gui.guiAction(window,t_w_draw,pulse_draw,t_b_draw,bpm_draw,ax1,ax2,fig1,fig2,loopNum) == 'exit':
                print("Exiting")
                window.close()
                sys.exit()
                
            # # wait for 1 second
            while (time.time() < lastMessage + 0.5):
                pass

            loopNum += 1
            lastMessage = time.time()
            
        # Should receive 2 messages / s, if less than this, reestablish comms
        commsResult = alrm.checkComms(lastMessage, serialPort, portName)
        if commsResult == True:
            loopNum = 0
            lasMessage = time.time()
            commsResult = False
        
else:
    print("Exiting")
    for e in sys.exc_info():
        print("  ",e)
