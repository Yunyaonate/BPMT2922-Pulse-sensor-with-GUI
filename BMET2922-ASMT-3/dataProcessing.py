"""
This file stores all the function to processign the data

Author: Yunyao Duan

Date:  11-11-2021
"""

from classDefine import data
from classDefine import alarm


def fourBytesToNum(dataType,this_message):
    """
    fourBytesToNum function:

    The raw message stores the data in bytes, where every 4 bytes represent a nubmer.
    This function is to transfer the 4-digital-chars into binary numbers, and store the numbers as int/float list to the correspond class for later use

    To deal with the data, we should force each byte be integer, find the corrensponding character (real nubmer), and transfer to integer
    When we get the number of each digital of a number, times the digit (1000, 100, 10, or 1) add them together

    Note that the BPM data should divide by 10 because we timed 10 when we sent the message

    After getting the data in integer/float of this message, append the data into the lists that store all the data 

    Input:  dataType, input raw message
    Output: Nil

    Author: Yunyao Duan
    """

    dataStartPo = 3     # The postion in the message that stores the data type info

    if dataType == ord('B'):
        i = dataStartPo
        this_bpm = int(chr(int(this_message[i]))) * 1000 + int(chr(int(this_message[i+1]))) * 100 + int(chr(int(this_message[i+2])))*10 + int(chr(int(this_message[i+3])))
        data.this_bpm = this_bpm / 10
        print("This is a BPM message: ",data.this_bpm)
        data.bpm.append(data.this_bpm)
        # print("All BPM", data.bpm)

    if dataType == ord('W'):
        print("This is a Pulse Waveform message:")
        dataSize = 50
        pulse = [0] * dataSize
        for j in range(dataSize):             # position in the pulse array
            i = dataStartPo + j*4             # position in the raw message
            pulse[j] = int(chr(int(this_message[i]))) * 1000 + int(chr(int(this_message[i+1]))) * 100 + int(chr(int(this_message[i+2]))) * 10 + int(chr(int(this_message[i+3])))            
        #     print(pulse[j],end=" ")
        # print(" ")
        data.this_pulse = pulse
        print(data.this_pulse)
        data.pulse = data.pulse + pulse
        # print("all puls:", data.pulse)


def meanBpm(bpmCnt):
    """
    mean BPM function:
    This function is to calculate the mean BPM over the last 15 seconds

    The bpmCnt count from 0 to 14, refers to the position we store a new BPM into the last_15_bpm array. 

    It increment by 1 every time a BPM message is received. 
    When bpmCnt is going to be larger than 14, make it back to 0, we use the new received BPM to re-write the position
    So the last_15_bpm array is always with size of 15, and stores the newest 15 BPMs

    Then, calculate the average of this array, we can get the mean BPM over the last 15 seconds

    Input:  bpmCnt
    Output: bpmCnt

    Author: Yunyao Duan
    """

    # Store this BPM to an array that stores the last 15 second bpm
    data.last_15_bpm[bpmCnt] = data.this_bpm

    # Calculate the mean BPM
    mean_bpm = sum(data.last_15_bpm)/15

    # Stores the mean BPM into the array that stores all the mean bpm
    data.mean_bpm.append(mean_bpm)
    print("Last 15 bpm: ", data.last_15_bpm)
    print("Mean BPM over last 15 seconds: %.2f" %round(mean_bpm))
    
    # Update the bpmCnt for the next position to write BPM
    bpmCnt +=1
    if bpmCnt >= 15:
        bpmCnt = 0
    return bpmCnt