import time
from classDefine import data
from classDefine import alarm

def seqnumCheck(this_message):
    newSeqNum = int(this_message[1])
    if newSeqNum == data.oldSeqNum + 1:
        data.oldSeqNum = newSeqNum
        if data.oldSeqNum > 255:
            data.oldSeqNum = 127
        return True
    else:
        # print("supposed sequence number: ", data.oldSeqNum + 1,"received sequence Number: ", newSeqNum)
        return False

## Check flags
def flagCheck(this_message):
    if int(this_message[0]) == 255 and int(this_message[-2]) == 255:
        #print(this_message[0])
        #print(this_message[-1])
        return True
    else:
        return False

## checksum function: return true if the received checksum and calculated checksum matched
def checksum(this_message):
    # get the checksum of the message
    checksumPo  = len(this_message) - 3
    checksum1 = int(this_message[checksumPo])

    # calculate the checksum
    sumVal = 0
    for i in range(checksumPo):
        # the int(chr(int(message))) is the corresponding char in decimal bytes 
        # e.g 65 (for 'A'), 49 (for '1')

        sumVal += int(this_message[i])
        # print(int(this_message[i]))         
    
    sumVal = sumVal & 255   
    checksum2 = int (sumVal | 128)

    # print("Add the decimal bytes before checksum: ",sumVal,"checksum: ",checksum2)
    # print("Compare the received checksum and calculated check sum:",checksum1,checksum2)

    if checksum1 == checksum2:
        return True
    else: return False

## Comms alarm: if no bpm for 5 sec, or wrong seqNum, wrong checksum, raise this alarm, 
#  if commsAlarm == False, the message can be stored to later use, else, reject this message
def commsAlarm(this_message):  
    current_time = time.time()
    if current_time - alarm.last_bpm_time > 5:
        alarm.alarm_string = "COMMs - No BPM"
        print(alarm.alarm_string)
        return True
    if seqnumCheck(this_message) == False:
        alarm.alarm_string = "COMMs - Sequence error"
        print(alarm.alarm_string)
        return True
    elif checksum(this_message) == False:
        alarm.alarm_string = "COMMs - Checksum error"
        print(alarm.alarm_string)
        return True
    else:
        # print("Comms validation: Pass")
        return False


def bpmAlarm(this_bpm):
    if this_bpm > alarm.highBpmThreshold:
        alarm.alarm_string = 'Pulse High'
        return True 
    elif this_bpm < alarm.lowBpmThreshold:
        alarm.alarm_string = 'Pulse Low'
        return True
    else: return False