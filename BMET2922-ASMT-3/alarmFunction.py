
"""
This file contains all the functions about the rasing alarms, including
- COMMs alarms (input message validation)(ALRM-1), 
- BPM alarms (determine if the BPM is out of the desired range)
- Check Comms (Detect if the Host and Arduino is connected, execute reconnecting or existing the program)

Author: Yunyao Duan and Jacinta Cleary
Date:   15-Nov-2021
"""

import time
from classDefine import data
from classDefine import alarm
import serial
from datetime import datetime


def seqnumCheck(this_message):
    """
    Sequence number check function:
    This function is to check if the sequence nubmer of this message is incremented by 1 to the last message

    The old sequence number is defined outside of this function, it is initialsed every time we reconnect the sensor (the first message), 
    which is received sequence nubmer -1, to make sure the sequence number of the first message is always correct

    For the rest of the message, we always check if the current sequence nubmer - old sequence = 1, and update the old sequence nubmer

    If there is sequence number error, this function will return False, otherwise, the function will return True


    Input:  This message
    Output: True or False

    Author: Jacinta Cleary
    """
    newSeqNum = int(this_message[1])
    if newSeqNum == data.oldSeqNum + 1:
        data.oldSeqNum = newSeqNum
        if data.oldSeqNum >= 255:
            data.oldSeqNum = 127
        return True
    else:
        if newSeqNum > data.oldSeqNum + 2:
            data.oldSeqNum = data.oldSeqNum + 1
        else:
            data.oldSeqNum = newSeqNum
        if data.oldSeqNum > 255:
            data.oldSeqNum = 127
        return False


def checksum(this_message):
    """
    checksum function: 
    get the checksum of the message (received checksum), and calculte the checksum of this message (calculated checksum)
    compare the received checksum and calculated checksum, if they are matched, return True, otherwise, return false

    Input:  input message
    Output: True or False

    Author: Yunyao Duan
    """
    # get the checksum of the message
    checksumPo  = len(this_message) - 3
    checksum1 = int(this_message[checksumPo])

    # calculate the checksum
    sumVal = 0
    for i in range(checksumPo):
        # Sum all the digits
        sumVal += int(this_message[i])
        # print(int(this_message[i]))         
    
    sumVal = sumVal & 255   
    checksum2 = int (sumVal | 128)

    # print("Add the decimal bytes before checksum: ",sumVal,"checksum: ",checksum2)
    # print("Compare the received checksum and calculated check sum:",checksum1,checksum2)

    if checksum1 == checksum2:
        return True
    else: return False


def commsAlarm(this_message):  
    """
    comms alarm:
    input message validation to meet the requirement ALRM-1

    if there's no BPM for 5 seconds, or wrong sequence number in the input message, or or checksum for the input message, raise this alarm
    if commsAlarm == False, the message can be stored to later use, else, reject this message

    if there's COMM error, change the alarm_string, if there's no COMM error, erase the alarm_string. 
    Note that we directly change the alarm_string in the class "alarm", we don't output the alarm string

    Input:  input message, last received BPM time
    Output: True or false

    Author: Yunyao Duan
    """

    # if current time - last received BPM time greater than 5s, write the alarm string, raise the comm alarm
    current_time = time.time()
    if current_time - alarm.last_bpm_time > 5:
        alarm.alarm_string = "COMMs - No BPM"
        print(alarm.alarm_string)
        alarm.last_bpm_time = time.time()
        return True

    # if there's sequence number error, write the alarm string, and raise the comm alarm
    if seqnumCheck(this_message) == False:
        alarm.alarm_string = "COMMs - Sequence error"
        print(alarm.alarm_string)
        return True
    
    # if there's checksum error, write the alarm string, and raise the comm alarm
    elif checksum(this_message) == False:
        alarm.alarm_string = "COMMs - Checksum error"
        print(alarm.alarm_string)
        return True
    
    # if there's no comm error, erase the alarm string
    else:
        alarm.alarm_string = ''
        return False


def bpmAlarm(this_bpm):
    """
    BPM alarm:
    input message validation to meet the requirement ALRM-2,3

    if the current BPM is higher than the high BPM threshold, change the alarm string to "Pulse high", and raise this alarm
    if the current BPM is lower than the low BPM threshold, change the string to "Pulse low", and raise this alarm

    if the output of this alarm is True, there is a BPM alarm, else, the BPM is ok

    Input:  current BPM
    Output: True or False

    Author: Yunyao Duan
    """
    if this_bpm > alarm.highBpmThreshold:
        alarm.alarm_string = 'Pulse High'
        return True 
    elif this_bpm < alarm.lowBpmThreshold:
        alarm.alarm_string = 'Pulse Low'
        return True
    else:
        alarm.old_string = ''
        alarm.alarm_string = ''
        return False
 
def checkComms(lastMessage, serialPort, portName):
    """
    Check Comms alarm:
    If it has been greater than 2s without a message input, close the port, and attempt to reconnect. 
            
    Input: time last message was received. Serial port information.
    Output: None
            
    Author: Jacinta Cleary
    """

    if (time.time() - lastMessage) > 2.0:
        for i in range(2000):
            try:
                serialPort.close()
                if serialPort.isOpen() == False:
                    print("Disconnected") 
                break
            
            except:
                print("Port close failed: " + portName)
                time.sleep(1)

        print("**************************************")
        print("** Serial port closed: {}".format(portName))
        print("**************************************")

        time.sleep(0.5)

        for i in range(10):
            try:
                print("Trying to reconnect...")
                time.sleep(1)
                serialPort.open()
                if serialPort.isOpen:
                    print("Connected")
                    time.sleep(2)
                    return True
                break

            except:
                print("Port open failed: " + portName) 
