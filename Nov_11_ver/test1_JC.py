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

# serialString = ""  # Used to hold data coming over UART
# portName = "COM6"          # PC format
#portName = "/dev/tty..."    # Mac format
portName = "/dev/tty.ESP32testG01-ESP32SPP"    # Mac format

import time
from classDefine import data
from classDefine import alarm

from dataProcessing import fourBytesToNum
from dataProcessing import meanBpm

# import PySimpleGUI as sg
import guiFunctions as gui
import alarmFunction as alrm


#************************ Initialise GUI window ***************************#
# Draw GUI window
window = gui.draw_GUI_window()

# Initialise the GUI
##current = {}
##event, values = window.read(timeout=0.1)

# Add figures to canvas
ax1, fig1 = gui.addFigure(window["__CANVAS1__"])
ax2, fig2 = gui.addFigure(window["__CANVAS2__"])


# define the serial port.
# specify parameters as needed
serialPort = serial.Serial()
serialPort.port=portName 
serialPort.baudrate=115200
serialPort.bytesize=8
serialPort.timeout=2 
serialPort.stopbits=serial.STOPBITS_ONE

data.raw = []
data.bpm = []
data.pulse = []
data.this_bpm = []
data.this_pulse = []
data.last_15_bpm = [0] * 15
data.mean_bpm = []

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

            ##********************** Start Main Loop Here*****************************

            timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            print("\nLoop Number: ",loopNum)
            # this_message = data.raw[loopNum]

            if loopNum == 0:
                data.oldSeqNum = this_message[1] - 1

            print("Last BPM Time = {}".format(alarm.last_bpm_time))
            if this_message == []:
                print("No message received")
            elif alrm.commsAlarm(this_message) == True:
                print("{} : {}".format(timestamp,alarm.alarm_string))
            else:
                print("input Message validation: Pass")
            
                #------------ Store the pulse data (transfer the "4-digit-char" into a single number)--------------
                dataType = int(this_message[2])
                fourBytesToNum(dataType,this_message)

                if dataType == ord('B'):
                    # mark the bpm received time
                    alarm.last_bpm_time = time.time()
                    print("Time BPM received = {}".format(alarm.last_bpm_time))

                    # print("bpm received time (in epoch): %.2f" %alarm.last_bpm_time)
                    
                    # mean bpm
                    bpmCnt = meanBpm(bpmCnt)
                    if alrm.bpmAlarm(data.this_bpm) == True:
                        print("{} : {}".format(timestamp,alarm.alarm_string))
                

            # ---------------------Till now, the data is ready to be printed------------------------------------------

            # Initialise data to draw
            t_w_draw, pulse_draw, t_b_draw, bpm_draw = gui.get_data_to_draw()

            # Now do GUI actions
            if gui.guiAction(window,t_w_draw,pulse_draw,t_b_draw,bpm_draw,ax1,ax2,fig1,fig2,loopNum) == 'exit':
                break

            # # wait for 1 second
            while (time.time() < lastMessage + 0.5):
                pass
            # while (time.time() < startTime + 0.5):
            #     pass

            # startTime += 0.5
            loopNum += 1

            #print(serialString.decode("Ascii"), end = "")
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
