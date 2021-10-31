import csv
import time
from classDefine import data
from classDefine import alarm
from classDefine import print_message
from alarmFunction import commsAlarm
from alarmFunction import bpmAlarm
from dataProcessing import fourBytesToNum
from dataProcessing import meanBpm

filename = 'messageExample.csv'

file = open(filename)
csvreader = csv.reader(file)

for row in csvreader:
    data.raw.append(row)
file.close()

# initialise the old sequence number as the first received sequcen number -1
data.oldSeqNum = int(data.raw[0][1]) - 1
# this_message = data.raw[0]
# print_message(this_message)

bpmCnt = 0
for loopNum in range(51):
    timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    print("\nLoop Number: ",loopNum)
    this_message = data.raw[loopNum]
    
    if commsAlarm(this_message) == True:
        print(timestamp, ": ", alarm.alarm_string)
    else:
        print("input Message validation: Pass")
    
        #------------ Store the pulse data (transfer the "4-digit-char" into a single number)--------------
        dataType = int(this_message[2])
        fourBytesToNum(dataType,this_message)

        if dataType == ord('B'):
            # mark the bpm received time
            alarm.last_bpm_time = time.time()
            # print("bpm received time (in epoch): %.2f" %alarm.last_bpm_time)
            
            # mean bpm
            bpmCnt = meanBpm(bpmCnt)
         
             # bpm alarm
            bpmAlarm(data.this_bpm)
            if bpmAlarm(data.this_bpm) == True:
                print(timestamp, ": ", alarm.alarm_string)



    
 