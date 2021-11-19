#!/usr/bin/env python
"""
Extract function names and information prefixed by **

Author: G.Watkins
Date:   01-Oct-2021
"""

import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

def search_for_file_path ():
    """
    Browse for a filename
    ref: https://stackoverflow.com/questions/19944712/browse-for-file-path-in-python

    Input:  Nil
    Output: selected file name

    Author: G.Watkins
    """
    
    currdir = os.getcwd()
    fname = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    return fname


fname = search_for_file_path()

if len(fname) == 0:
    print("No file selected")
else:
    print ("File: ", fname)
    f = open(fname)
    lines = f.readlines()
    f.close()

    start = True    # used to track start of a header section
    for line in lines:
        if "**" in line:
            if start:
                print("======") # delimit header sections
                start = False
            print(line.lstrip(), end="")    # header line. Already contains new line.
        else:
            start = True
