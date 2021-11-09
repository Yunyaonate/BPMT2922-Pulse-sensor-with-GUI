from classDefine import data
from classDefine import alarm

## This function transfer the 4-digital-chars into numbers, and store the numbers as int/float list into the class
def fourBytesToNum(dataType,this_message):
    dataStartPo = 3

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
        for j in range(dataSize):         # position in the pulse array
            i = dataStartPo + j*4             # position in the raw message
            pulse[j] = int(chr(int(this_message[i]))) * 1000 + int(chr(int(this_message[i+1]))) * 100 + int(chr(int(this_message[i+2]))) * 10 + int(chr(int(this_message[i+3])))
        #     print(pulse[j],end=" ")
        # print(" ")
        data.this_pulse = pulse
        print(data.this_pulse)
        data.pulse = data.pulse + pulse
        # print("all puls:", data.pulse)

## calculate mean bpm by storing the new bpm in the bpmCnt position of the last_15_bpm array
# return the next bpm position to write into the array
def meanBpm(bpmCnt):
    # mean bpm over last 15 sec
    data.last_15_bpm[bpmCnt] = data.this_bpm
    mean_bpm = sum(data.last_15_bpm)/15
    data.mean_bpm.append(mean_bpm)
    print("Last 15 bpm: ", data.last_15_bpm)
    print("Mean BPM over last 15 seconds: %.2f" %round(mean_bpm))
    bpmCnt +=1
    if bpmCnt >= 15:
        bpmCnt = 0
    return bpmCnt