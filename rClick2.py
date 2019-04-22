#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 20161215

@author: g00377630
'''
import tkinter as tk
import MessageBox
from tkinter import *

def rClicker2_ListBox(e,root):

        try:
            def rClick_Delete(e):
                try:
                    e.widget.delete(0,END)
                except ValueError:
                    MessageBoxFail = MessageBox.Mbox
                    MessageBoxFail.root = root
                    MessageBoxFail('Error in Clear feedback message!')
                return
            e.widget.focus()
            nclst=[
                   ('Clear',lambda e=e:rClick_Delete(e))
                   ]
    
            rmenu = tk.Menu(None, tearoff=0, takefocus=0)
    
            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)
                rmenu.add_separator()
    
            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
    
        except TclError:
            print (' - rClick menu, something wrong')
            pass
    
        return "break"
