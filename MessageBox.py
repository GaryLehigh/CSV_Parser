#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2016 12 14

@author: g00377630

'''
import tkinter
from tkinter import ttk
class Mbox(object):

    root = None

    def __init__(self, msg, dict_key=None):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        tk = tkinter
        self.top = tk.Toplevel(Mbox.root)
        w = 400 # width for the Tk root
        h = 200 # height for the Tk root
        # get screen width and height
        ws = self.top.winfo_screenwidth() # width of the screen
        hs = self.top.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x_mainWindow = (ws/2) - (w/2)
        y_mainWindow = (hs/2) - (h/2)
        self.top.geometry('%dx%d+%d+%d' % (w, h, x_mainWindow, y_mainWindow))
        self.top.resizable(width=False, height=False)

        frm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        label = tk.Label(frm, text= msg, width = 400, wraplength = 300)
        label.pack(padx=4, pady=40)

        caller_wants_an_entry = dict_key is not None

        if caller_wants_an_entry:
            self.entry = tk.Entry(frm)
            self.entry.pack(pady=4)

            b_submit = tk.Button(frm, text='OK')
            b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            b_submit.pack()

        b_cancel = tk.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, dict_key):
        data = self.entry.get()
        if data:
            d, key = dict_key
            d[key] = data
            self.top.destroy()
            

class ProgressBox(object):

    root = None
    def __init__(self, valueLowerBound = 0, valueHigherBound = 100, dict_key=None):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        tk = tkinter
        self.top = tk.Toplevel(Mbox.root)
        w = 400 # width for the Tk root
        h = 200 # height for the Tk root
        # get screen width and height
        ws = self.top.winfo_screenwidth() # width of the screen
        hs = self.top.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x_mainWindow = (ws/2) - (w/2)
        y_mainWindow = (hs/2) - (h/2)
        self.top.geometry('%dx%d+%d+%d' % (w, h, x_mainWindow, y_mainWindow))
        self.top.resizable(width=False, height=False)

        frm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)


        self.progressBar = ttk.Progressbar(frm, orient = 'horizontal', length = 200,mode = "determinate")
        self.progressBar['value'] = valueLowerBound
        self.progressBar['maximum'] = valueHigherBound
        self.progressBar.pack(padx=4, pady=40)
        
        caller_wants_an_entry = dict_key is not None

        if caller_wants_an_entry:
            self.entry = tk.Entry(frm)
            self.entry.pack(pady=4)

            b_submit = tk.Button(frm, text='OK')
            b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            b_submit.pack()

        b_cancel = tk.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, dict_key):
        data = self.entry.get()
        if data:
            d, key = dict_key
            d[key] = data
            self.top.destroy()   
            
    def quit(self):
        self.top.destroy()              
            
