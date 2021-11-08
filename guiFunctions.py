
from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
# import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use('TkAgg')
import time

from classDefine import data
from classDefine import alarm

## ********* Figure plotting parameter ***************
# set up GUI window size
WIN_WIDTH = 800
WIN_HEIGHT = 750

# Parameters for pulse waveform plotting
dt_w = 0.02
STEP = 50                   # how many points we move in each frame
DATALEN_w = STEP * 15         # how many points we print in one frame = window width

# For BPM
dt_b = 1
DATALEN_b = 15


def get_this_array(data_all,dt,DATALEN):
    '''
    Only strach the desired part with the required lenth of array from all data
    Author: Yunyao Duan
    '''
    t_all      = [j*dt for j in range(len(data_all))]

    if len(data_all) < DATALEN:
        data_this = data_all
        t_this = t_all
    else:   
        data_this  = data_all
        t_this     = t_all

    return t_all, t_this, data_this

def update_arrays(data_all,t_all,data_this,t_this,DATALEN):
    if len(data_all) > DATALEN:
        data_this = data_all[-DATALEN:]
        t_this = t_all[-DATALEN:]
    else:
        data_this = data_all
        t_this = t_all

    return data_this, t_this

def get_data_to_draw():
    [t_w_all,t_w_this,pulse_this] = get_this_array(data.pulse,dt_w,DATALEN_w)
    [pulse_this,t_w_this] = update_arrays(data.pulse,t_w_all,pulse_this,t_w_this,DATALEN_w)

    [t_b_all,t_b_this,bpm_this] = get_this_array(data.bpm,dt_b,DATALEN_b)
    [bpm_this,t_b_this] = update_arrays(data.bpm,t_b_all,bpm_this,t_b_this,DATALEN_b)

    return t_w_this, pulse_this, t_b_this, bpm_this

def draw_GUI_window():
    tab_layout = [  [sg.Button("Exit",key = "Exit",font=('Helvetica', 20))],
            [sg.TabGroup([[sg.Tab('Pulse Waveform', [[sg.Canvas(key="__CANVAS1__", size=(5,4))]]), sg.Tab('BPM', [[sg.Canvas(key="__CANVAS2__", size=(5,4))]])]])],        
            ]


    window = sg.Window("Window name", tab_layout, size = (WIN_WIDTH,WIN_HEIGHT),finalize=True,element_justification='center', font='Helvetica 16')
    return window

def addFigure(canvasElement):
    # create a figure
    fig = Figure()
    # create a set of axes on the figure 
    ax = fig.add_subplot(1,1,1)

    # place the figure on the canvas
    canvas = canvasElement.TKCanvas
    figAgg = FigureCanvasTkAgg(fig, canvas)
    figAgg.draw()
    figAgg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return ax, figAgg

def plotFigure(ax,fig,t,ydata,dataType,DATALEN):
    ax.cla()

    if dataType == 'W':
        ax.plot(t,ydata,linewidth =1)
        ax.set_ylabel('Pulse Waveform')

    elif dataType == 'B':
        h_thre = [alarm.highBpmThreshold] * len(t)
        l_thre = [alarm.lowBpmThreshold] * len(t)
        line1, = ax.plot(t,h_thre,color = 'red',label = 'High BPM Threshold')
        line2, = ax.plot(t,l_thre,color = 'orange',label = 'Low BPM Threshold')
        ax.legend(handles=[line1,line2],bbox_to_anchor=(0., 1.03, 1., .103),borderaxespad=0.)
        ax.bar(t,ydata)
        ax.set_ylabel('BPM')

    ax.set_xlabel("time")
    ax.set_ylim([min(ydata)*0.95-1,max(ydata)*1.05+1])

    if len(t) < DATALEN:
        ax.set_xlim([0,15])

    fig.draw()
    return ax


def guiAction(window,t_w_this,pulse_this,t_b_this,bpm_this,ax1,ax2,fig1,fig2):  
    if True: 
        print("yes it is true")
        event, values = window.read(0.1)
        if event == sg.WIN_CLOSED or event == 'Exit':
            return 'exit'

        if len(pulse_this)!= 0:
            plotFigure(ax1, fig1,t_w_this,pulse_this,"W",DATALEN_w)

        if len(bpm_this) != 0:
            plotFigure(ax2, fig2,t_b_this,bpm_this,"B",DATALEN_b)
        
        # canvas = '__CANVAS1__'
        # legend_text = """
        #         -------------------
        #         |   ------     line1    |
        #         |   ------     line2    |
        #         |   ------     line3    |
        #         -------------------"""
        # legend_frame = LabelFrame(canvas,text='Legend',padx=5, pady=5)
        # legend_label = Label(legend_frame,text=legend_text)
        # legend_label.pack()
        # canvas.create_window(120,200,window=legend_frame)
        
