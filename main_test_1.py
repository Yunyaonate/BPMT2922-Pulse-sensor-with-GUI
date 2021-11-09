
import time
from classDefine import data
from classDefine import alarm

from dataProcessing import fourBytesToNum
from dataProcessing import meanBpm

import PySimpleGUI as sg
import guiFunctions as gui
import alarmFunction as alrm


#************************ Initialise GUI window ***************************#
# Draw GUI window
window = gui.draw_GUI_window()

# Initialise the GUI
current = {}
event, values = window.read(timeout=0.1)

# Add figures to canvas
ax1, fig1 = gui.addFigure(window["__CANVAS1__"])
ax2, fig2 = gui.addFigure(window["__CANVAS2__"])

#************************** DATA PROCESSING ***********************************
bpmCnt = 0
loopNum = 0

startTime   = time.time()
#*************************** MAIN LOOP ************************************
while loopNum < 60:
 
    timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())


    print("\nLoop Number: ",loopNum)
    this_message = data.raw[loopNum]

    if this_message == []:
        print("No message received")
    elif alrm.commsAlarm(this_message) == True:
        print("{} : {}".format(timestamp,alarm.alarm_string))
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

            if alrm.bpmAlarm(data.this_bpm) == True:
                print("{} : {}".format(timestamp,alarm.alarm_string))
        

    # ---------------------Till now, the data is ready to be printed------------------------------------------

    # Initialise data to draw
    t_w_draw, pulse_draw, t_b_draw, bpm_draw = gui.get_data_to_draw()
  
    # Now do GUI actions
    if gui.guiAction(window,current,values,t_w_draw,pulse_draw,t_b_draw,bpm_draw,ax1,ax2,fig1,fig2) == 'exit':
        break

    # wait for 1 second
    while (time.time() < startTime + 0.5):
        pass

    startTime += 0.5
    loopNum += 1








    
 