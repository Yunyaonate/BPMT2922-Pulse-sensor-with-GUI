import time
import csv

HIGH_BPM_DEFAULT = 90
LOW_BPM_DEFAULT = 40

class data:
    raw = []
    bpm = []
    pulse = []
    this_bpm = []
    this_pulse = []
    last_15_bpm = [0] * 15
    mean_bpm = []
    pass

class alarm:
    alarm_string = ""
    highBpmThreshold = HIGH_BPM_DEFAULT
    lowBpmThreshold = LOW_BPM_DEFAULT
    last_bpm_time = time.time()

def print_message(this_message):
    ### This part is supposed to be in the loop, we put it outside to just check for the one of the message
    # Print out this data:
    print("Print the input message in Char: ")
    for i in range(len(this_message)):
        if i == 1 or i == len(this_message)-3:
            print(this_message[i],end=" ")   
        elif i == 0 or i%4 == 2:
            print(chr(int(this_message[i])),end=" ")
        else: 
            print(chr(int(this_message[i])),end="")
    print("\n")

    # Print the input message in decimal bytes:
    print("Print the input message in decimal bytes: ")
    for i in range(len(this_message)):
        print((int(this_message[i])),end=" ")
    print("\n")

filename = 'messageExample1.csv'
file = open(filename)
csvreader = csv.reader(file)

for row in csvreader:
    data.raw.append(row)
file.close()


# Initialise the old sequence number as the first received sequcen number -1
data.oldSeqNum = int(data.raw[0][1]) - 1
