#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 20161215

@author: g00377630
'''
import tkinter as tk
import MessageBox
from tkinter import *

def rClicker_ListBox(e,fileList,root):

        try:
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')
                
                
            def rClick_Cut(e):
                e.widget.event_generate('<Control-c>')
                rClick_Delete(e)
                
                
            
            def rClick_Delete(e):
                fileName =  e.widget.get(tk.ANCHOR)
                if fileName == '':
                    MessageBoxFail = MessageBox.Mbox
                    MessageBoxFail.root = root
                    MessageBoxFail('Please select a file!')
                realFileName = fileName[15:]
                try:
                    fileList.remove(realFileName) 
                    e.widget.delete(ANCHOR) 
                except ValueError:
                    MessageBoxFail = MessageBox.Mbox
                    MessageBoxFail.root = root
                    MessageBoxFail('File is not in the List')
                return
                    
            e.widget.focus()
    
            nclst=[
                   (' Cut', lambda e=e: rClick_Cut(e)),
                   (' Copy', lambda e=e: rClick_Copy(e)),
                   ('Delete',lambda e=e:rClick_Delete(e))
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
    
