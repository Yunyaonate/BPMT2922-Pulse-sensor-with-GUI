"""
This file is to define all the classes we need in the program

The reason why we use class is, using class can help us to better manage the patient's information when there're more than one patient

The other reason is, for some alarm functions, we only want one output, True or False, so it can be a condition for if statement, 
but we need to change the value of some variable, so we use a class, to change it inside of a function but don't need to output it

Author: Yunyao Duan

Date:  11-11-2021
"""
import time

# Set up the default value of the BPM thresholds
HIGH_BPM_DEFAULT = 90
LOW_BPM_DEFAULT = 40

class data:
    raw = []                # To store all the raw data
    bpm = []                # To store all the bpm data
    pulse = []              # To store all the pulse data
    this_bpm = []           # To store the current bpm data
    this_pulse = []         # To store the current pulse data
    last_15_bpm = [0] * 15  # Initialise an array of 15 to store the last 15 BPM
    mean_bpm = []           # To store the mean BPMs
    pass

class alarm:
    alarm_string = ""       # To store the alarm string
    old_string = ""         # To store the old alarm string, so we can detect the state change
    highBpmThreshold = HIGH_BPM_DEFAULT     # Initialise the high BPM threshold as default value
    lowBpmThreshold = LOW_BPM_DEFAULT       # Initialise the low BPM threshold as the defaulte value
    last_bpm_time = time.time() 

