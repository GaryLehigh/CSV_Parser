#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2016 12 8

@author: g00377630
'''
import csv;
import math;
import tkinter as tk;
from tkinter import *

import MessageBox
import rClick
import rClick2

from tkinter import filedialog
from tkinter import font
from tkinter import ttk
import CSVAnalyserSingleFileMode  as csvAnalyserS
import CSVAnalyserMultiFileMode  as csvAnalyserM
import os
from distutils.filelist import FileList
import time
import threading
from multiprocessing.pool import ThreadPool


root = tk.Tk()
w = 520 # width for the Tk root
h = 650 # height for the Tk root
w_subPatternSelectionWindow = 500
h_subPatternSelectionWindow = 400
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x_mainWindow = (ws/2) - (w/2)
y_mainWindow = (hs/2) - (h/2)
x_subPatternSelectionWindow = (ws/2) - (w_subPatternSelectionWindow/2)
y_subPatternSelectionWindow = (hs/2) - (h_subPatternSelectionWindow/2)


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


root.geometry('%dx%d+%d+%d' % (w, h, x_mainWindow, y_mainWindow))
root.resizable(width=False, height=False)

#Regular expression for suitable files
filenamePattern = re.compile('.+\.(csv|xls|xlsx|xlsm|xlsb|txt)$')


filenamePattern2 = re.compile('.+\.(txt)$')



class Application(tk.Frame):
    listBox = tk.Listbox(root, width = 85, height =14,bg='#CCE8CF')
    resultListBox = tk.Listbox(root, width = 85, height =7, bg = '#CCE8CF')
    menuBar = tk.Menu(root,relief="raised")
    textFilePath = tk.Text(root, width =65,height =1)
    browseButton = tk.Button(root, text = "Browse")
    addFileButton = tk.Button(root, text='Add File')
    menubutton = tk.Menubutton(root, text="Select Compare Mode",
                                   indicatoron=True, borderwidth=1, relief="raised")
    menuSelection= tk.Menu(menubutton, tearoff=False)
    openSelectionWindowButton =tk.Button(root, text="Select Compare Mode")
    helv36 = tk.font.Font(family="Helvetica",size=16,weight="bold")
    helv18 = tk.font.Font(family="Helvetica",size=8,weight="bold")

    #Single File Mode
    singleFilePatternChoices = ["Dlsch_Curt_Csv_T034", "Dest_T035_TTI_TYPE_EPDCCH_FULL", "Dest_T052_TTI_TYPE_EPDCCH_ECCERES_RES", "Compare Mode 4",
                                 "Compare Mode 5", "Compare Mode 6"]
    fixedSingleFilePatternNum = 0
    customSingleFilePatternNum = 0
    singleFilePatternChoicesMap = {}
    #Custom File input
    customFilePatternContentMap = {}


    multiFilesPatternChoices = ("34_35_1", "34_52_1", "Multi-Compare Mode 3")
    multiFilesPatternChoicesMap = {}

    entireChoiceSet =[]
    entireChoiceSet.append(singleFilePatternChoices)
    entireChoiceSet.append(multiFilesPatternChoices)

    entireMapSet =[]
    entireMapSet.append(singleFilePatternChoicesMap)
    entireMapSet.append(multiFilesPatternChoicesMap)

    singleFilePatternLabels = []
    singleFilePatternCheckButtons = []

    customPatternLabels = []
    customPatternDeleteButton = []

    multiFilesPatternLabels = []
    multiFilesPatternCheckButtons = []

    fileList= []
    customPatternFileList = []
    fileIndex = 1
    destinationFolderName = ''
    customI = 0
    '''
    0 means Single File Compare
    1 means Multiple Files Compare
    '''
    compareMode = 0
    analyzeButton = tk.Button(root, text = 'Analyze', height = 2, width = 10, bg = '#FFDB38',
                              font =helv36)


    def __init__(self, master=root):
        tk.Frame.__init__(self, master,width = screen_width/2, heigh =screen_height/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x_mainWindow, y_mainWindow))
        root.resizable(width=False, height=False)

        root.rowconfigure(0, weight = 1)
        root.rowconfigure(1, weight = 3)
        root.rowconfigure(2, weight = 8)
        root.rowconfigure(3, weight = 3)
        root.columnconfigure(0, weight = 8)
        root.columnconfigure(1, weight = 1)
        root.columnconfigure(2, weight = 2)
        self.createAddFileWidgets()
        self.createListBoxWidgets()
        self.createMenu()
        self.createBrowseFolderWidgets()
        self.createPatternSelectionWindowWidgets()
        self.createAnalyzeButton()
        self.createResultListBoxWidgets()
        root.protocol('WM_DELETE_WINDOW', self._quit)


    def _quit(self):
        root.quit()      # Close the window
        root.destroy()   # destroy all widgets and recycle the memory


    def _quit_SubWindow(self):
        for fileName in self.customPatternFileList:
            #Read File Into Map
            patternDict = {}
            i = 0
            nextIndex = 0;
            with open(fileName, 'r') as f:
                for line in f:
                    pureLine = line.strip()
                    if pureLine == '':
                        continue
                    else:
                        if(i%2 == 0):
                            nextIndex = float(line.strip())
                        else:
                            patternDict[nextIndex]= line.split('\n')[0]
                    i = i + 1
            f.close()
            self.customFilePatternContentMap[fileName] = patternDict
        self.openSelectionWindowButton.config(state = 'normal')
        self.window.withdraw()

    #quit custom compare mode input window
    def _quit_SubWindow2(self):
        '''delete inexsiting compare mode
        print (self.fixedSingleFilePatternNum)
        print (len(self.singleFilePatternLabels))
        print (self.customSingleFilePatternNum)
        print ()
        '''
        print ('len', len(self.customFilePatternContentMap))
        for i in range(0, self.customSingleFilePatternNum):
            self.singleFilePatternLabels[-1].grid_forget()
            self.singleFilePatternCheckButtons[-1].grid_forget()
            del self.singleFilePatternLabels[-1]
            del self.singleFilePatternCheckButtons[-1]
            self.reConfigWindow(-25)
        self.customSingleFilePatternNum = 0
        self.i = self.fixedSingleFilePatternNum

        for fileName in self.customPatternFileList:
            self.singleFilePatternChoicesMap[fileName] = tk.IntVar(value = 0)
            self.customSingleFilePatternNum = self.customSingleFilePatternNum + 1
            #Read File Into Map
            patternDict = {}
            i = 0
            nextIndex = 0;
            with open(fileName, 'r') as f:
                for line in f:
                    pureLine = line.strip()
                    if pureLine == '':
                        continue
                    else:
                        if(i%2 == 0):
                            nextIndex = float(line.strip())
                        else:
                            patternDict[nextIndex]= line.split('\n')[0]
                    i = i + 1
            f.close()
            self.customFilePatternContentMap[fileName] = patternDict
            self.singleFilePatternLabels.append(ttk.Label(self.window,text=fileName, width =40))
            self.singleFilePatternCheckButtons.append(ttk.Checkbutton(self.window, onvalue=2, offvalue=0,
                                    variable=self.singleFilePatternChoicesMap[fileName], command = self.printValues  ))
            self.window.rowconfigure(self.i, weight = 5)
            self.singleFilePatternLabels[-1].grid( padx = 50, pady = 10, row = self.i, column = 0)
            self.singleFilePatternCheckButtons[-1].grid(padx = 10, pady = 10, row = self.i, column = 1)
            self.i = self.i + 1
            self.window.rowconfigure(self.i, weight = 20)
            self.switchButton.grid(padx = 10, pady = 1, row = self.i, column = 0)
            self.quitButton.grid(padx = 1, pady = 10, row = self.i+1, column = 1, sticky = tk.S + tk.E)
            self.inputButton.grid(padx = 10, pady = 1, row = self.i+1, column = 0)
            self.clearButton.grid(padx = 10, pady = 1, row = self.i, column = 1, sticky = tk.E)
            self.reConfigWindow(25)


        self.inputButton.config(state = 'normal')
        self.windowPatternInput.withdraw()
        self.window.focus_force()


    def reConfigWindow(self, size):
        global ws, hs, h_subPatternSelectionWindow, w_subPatternSelectionWindow
        h_subPatternSelectionWindow = h_subPatternSelectionWindow + size
        # get screen width and height

        x_subPatternSelectionWindow = (ws/2) - (w_subPatternSelectionWindow/2)
        y_subPatternSelectionWindow = (hs/2) - (h_subPatternSelectionWindow/2)
        self.window.geometry('%dx%d+%d+%d' % (w_subPatternSelectionWindow,
                                      h_subPatternSelectionWindow,
                                      x_subPatternSelectionWindow,
                                      y_subPatternSelectionWindow))


    def deleteCustomPattern(self,index):
        try:
            self.customPatternDeleteButton[index].grid_forget()
            self.customPatternLabels[index].grid_forget()
            self.customI = self.customI - 1
            del  self.customPatternLabels[index]
            del  self.customPatternDeleteButton[index]
            del  self.customPatternFileList[index]
            print (self.customPatternFileList[index])
            for index in range(0, self.customI):
                self.customPatternLabels[index].grid(padx = 50, pady = 10, row = index, column = 0)
                self.customPatternDeleteButton[index].grid(padx = 10, pady = 10, row = index, column = 1)
                self.customPatternDeleteButton[index].configure(command = lambda: self.deleteCustomPattern(index))

            print ('self.customI = ', self.customI)
            self.browseButton.grid(padx = 1, pady = 10, row = self.customI, column = 0, sticky = tk.S + tk.E)
            self.customQuitButton.grid(padx = 1, pady = 10, row = self.customI, column = 1, sticky = tk.S + tk.E)
        except IndexError:
            return

    def checkFileExist(self,fileName):
        self.index1 = -1
        try:
            self.index1 = self.fileList.index(fileName)
        except ValueError:
            self.index1 = -1

        if self.index1 == -1:
            return 0
        else:
            return 1

    def checkCustomPatternExist(self, fileName):
        try:
            index1 = self.customPatternFileList.index(fileName)
        except ValueError:
            index1 = -1
        if index1 == -1:
            return 0
        else:
            return 1

    def checkFileName(self,fileName):
        if os.path.isfile(fileName) == 0:
            return 0
        else :
            match = filenamePattern.match(fileName)
            if match:
                if self.checkCustomPatternExist(fileName):
                    return 2
                else:
                    return 1
            else:
                return 0

    def checkCustomPatternName(self,fileName):
        if os.path.isfile(fileName) == 0:
            return 0
        else :
            match = filenamePattern2.match(fileName)
            if match:
                if self.checkCustomPatternExist(fileName):
                    return 2
                else:
                    return 1
            else:
                return 0

    def addFile(self):
        try:
            fileName = filedialog.askopenfilename(initialdir = 'D:\\python workspace2\\CsvReader\\CsvReader\\testCsvFiles')
        except:
            fileName = filedialog.askopenfilename(initialdir = 'C:\\')
        result = self.checkFileName(fileName)
        if(result == 1):
            self.fileList.append(fileName)
            strIndex = str(self.fileIndex) +"."
            fileWholeName = "{:15s}".format(strIndex)  + fileName
            self.listBox.insert(END, fileWholeName)
            self.fileIndex = self.fileIndex + 1
            return 1

        elif result == 2:
            MessageBoxFail = MessageBox.Mbox
            MessageBoxFail.root = root
            MessageBoxFail('The File Has Been Added!')
            self.windowPatternInput.focus_force()

        else:
            if fileName !='':
                MessageBoxFail = MessageBox.Mbox
                MessageBoxFail.root = root
                MessageBoxFail('Incorrect File Name!')


    def addPattern(self,pattern):
        self.patternSelection.append(pattern)

    def clearPatternMap(self):
        for choice in self.multiFilesPatternChoices:
            self.multiFilesPatternChoicesMap[choice].set(0)
        for choice in self.singleFilePatternChoicesMap:
            self.singleFilePatternChoicesMap[choice].set(0)

    def browseFolder(self):
        self.destinationFolderName = filedialog.askdirectory(initialdir = 'C:/Python27')
        self.textFilePath.delete('1.0', END)
        self.textFilePath.insert(END,self.destinationFolderName)

    def analyseCsvFiles(self):
        print ('\n\n')
        print ('')
        fileListTemp = []
        fileNameTemp =''
        for fileName in self.fileList:
            fileNameTemp = fileName
            fileListTemp.append(fileNameTemp.replace('/','\\'))


        #thrdPool = ThreadPool (processes = 1)
        #async_result = thrdPool.apply_async(csvAnalyser.Analyse,(fileListTemp, self.singleFilePatternChoicesMap, 
                                      #self.destinationFolderName, root, prgBox, self.compareMode))
        prgBox = MessageBox.ProgressBox(0)
        prgBox.root = root
        if(self.compareMode == 0):
            thrd1 = threading.Thread(target =csvAnalyserS.Analyse , args= (fileListTemp,self.customFilePatternContentMap, self.singleFilePatternChoicesMap,
                                                                                            self.destinationFolderName, root, self.resultListBox, prgBox))
            thrd1.start()
            #thrd2 = threading.Thread(target =csvAnalyserS.Analyse , args= (fileListTemp, {'Dlsch_Curt_Csv_T034': self.singleFilePatternChoicesMap['Dlsch_Curt_Csv_T034']}, 
            #                                                            self.destinationFolderName, root, self.resultListBox, prgBox))
            #thrd2.start()

        elif self.compareMode == 1 :
            thrd1 = threading.Thread(target =csvAnalyserM.Analyse , args= (fileListTemp, self.multiFilesPatternChoicesMap,
                                                                          self.destinationFolderName, root, self.resultListBox, prgBox))
            thrd1.start()
        #result = csvAnalyser.Analyse(fileListTemp, self.singleFilePatternChoicesMap, 
                                     # self.destinationFolderName, root, prgBox, self.compareMode )





    def switchCompareMode(self):
        self.compareMode = 1 - self.compareMode
        if(self.compareMode == 1):
            self.switchToMultiFilesMode()
        else:
            self.switchToSingleFileMode()

    def switchToSingleFileMode(self):
        jj = 0
        ii = 0
        self.switchButton.config(text = 'Switch to Multi-file Mode')

        for jj in range(0, self.j):
            self.multiFilesPatternLabels[jj].grid_forget()
            self.multiFilesPatternCheckButtons[jj].grid_forget()
        for ii in range(0, self.i):
            self.singleFilePatternLabels[ii].grid(padx = 50, pady = 10, row = ii, column = 0)
            self.singleFilePatternCheckButtons[ii].grid(padx = 10, pady = 10, row = ii, column = 1)
        self.inputButton.grid(padx = 10, pady = 1, row = ii+2, column = 0)

    def switchToMultiFilesMode(self):
        jj = 0
        ii = 0
        self.switchButton.config(text =  'Switch to Single-file Mode')
        for ii in range(0, self.i):
            self.singleFilePatternLabels[ii].grid_forget()
            self.singleFilePatternCheckButtons[ii].grid_forget()
        self.inputButton.grid_forget()
        for jj in range(0, self.j):
            self.multiFilesPatternLabels[jj].grid(padx = 50, pady = 10, row = jj, column =0, columnspan =1)
            self.multiFilesPatternCheckButtons[jj].grid(padx = 10, pady = 10, row = jj, column = 1)


    #Create Compare-Mode selection window
    def createSelectionWindow(self):
        self.openSelectionWindowButton.config(state = 'disable')
        if (not hasattr(self, 'window')):

            self.window = tk.Toplevel(root)
            self.window.protocol('WM_DELETE_WINDOW', self._quit_SubWindow)
            self.window.title('Compare Mode Selection')
            self.window.geometry('%dx%d+%d+%d' % (w_subPatternSelectionWindow,
                                                  h_subPatternSelectionWindow,
                                                  x_subPatternSelectionWindow,
                                                  y_subPatternSelectionWindow))
            #self.window.columnconfigure(0, weight =1)
            self.i = 0
            self.j = 0
            for choice in self.singleFilePatternChoices:
                self.singleFilePatternChoicesMap[choice] = tk.IntVar(value = 0)
                #char = 'Single-file Compare   ' + str(self.i)+ '   '
                char = choice
                self.singleFilePatternLabels.append(ttk.Label(self.window,text=char, width =40))
                self.singleFilePatternCheckButtons.append(ttk.Checkbutton(self.window, onvalue=1, offvalue=0,
                                        variable=self.singleFilePatternChoicesMap[choice], command = self.printValues  ))
                self.singleFilePatternLabels[-1].grid( padx = 50, pady = 10, row = self.i, column = 0)
                self.singleFilePatternCheckButtons[-1].grid(padx = 10, pady = 10, row = self.i, column = 1)
                #self.singleFilePatternLabels[-1].grid_forget()
                #self.singleFilePatternLabels[-1].grid()
                self.i = self.i + 1

            for choice in self.multiFilesPatternChoices:
                self.multiFilesPatternChoicesMap[choice] = tk.IntVar(value = 0)
                char = 'Multi-files Compare ' + str(self.j)+ ':  ' + choice
                self.multiFilesPatternLabels.append(ttk.Label(self.window, text=char, width =40))
                self.multiFilesPatternCheckButtons.append(ttk.Checkbutton(self.window, onvalue=1, offvalue=0,
                                        variable=self.multiFilesPatternChoicesMap[choice], command = self.printValues1  ))
                self.multiFilesPatternLabels[-1].grid(padx = 50, pady = 10, row = self.j, column = 0)
                self.multiFilesPatternCheckButtons[-1].grid(padx = 10, pady = 10, row = self.j, column = 1)
                self.j = self.j + 1


            self.fixedSingleFilePatternNum = self.i
            for jj in range(0, self.j):
                self.multiFilesPatternLabels[jj].grid_forget()
                self.multiFilesPatternCheckButtons[jj].grid_forget()
            self.switchButton = tk.Button(self.window, text = 'Switch to Multi-file Mode',  command = self.switchCompareMode)
            self.switchButton.grid(padx = 10, pady = 1, row = self.i, column = 0)
            self.quitButton = tk.Button(self.window, text= 'Confirm', command = self._quit_SubWindow, height = 1,
                           width = 8, bg = '#FFDB38',font =self.helv36 )
            self.window.rowconfigure(self.i, weight = 20)
            self.quitButton.grid(padx = 1, pady = 10, row = self.i+1, column = 1, sticky = tk.S + tk.E)
            self.inputButton = tk.Button(self.window, text = 'Input Compare Mode',  command = self.createMultiPatternInputWindow)
            self.inputButton.grid(padx = 10, pady = 1, row = self.i+1, column = 0)
            self.clearButton = tk.Button(self.window,text = 'Clear',command = self.clearPatternMap)
            self.clearButton.grid(padx = 10, pady = 1, row = self.i, column = 1, sticky = tk.E)

        else:
            self.window.deiconify()

    def createMultiPatternInputWindow(self):
        self.inputButton.config(state = 'disable')
        if (not hasattr(self, 'windowPatternInput')):
            self.windowPatternInput = tk.Toplevel(self.window)
            self.windowPatternInput.protocol('WM_DELETE_WINDOW', self._quit_SubWindow2)
            self.windowPatternInput.title('Compare Mode Input')
            self.windowPatternInput.geometry('%dx%d+%d+%d' % (w_subPatternSelectionWindow,
                                                  h_subPatternSelectionWindow,
                                                  x_subPatternSelectionWindow,
                                                  y_subPatternSelectionWindow))
            self.browseButton = tk.Button(self.windowPatternInput, text= 'Browse', height = 1,
                           width = 8,font =self.helv36, command = self.browseCustomPattern )
            self.browseButton.grid(padx = 1, pady = 10, row = 0, column = 0, sticky = tk.S + tk.E)
            self.customQuitButton = tk.Button(self.windowPatternInput, text= 'Confirm', command = self._quit_SubWindow2, height = 1,
                           width = 8, bg = '#FFDB38',font =self.helv36 )
            self.customQuitButton.grid(padx = 1, pady = 10, row = 0, column = 1, sticky = tk.S + tk.E)
        else:
            self.windowPatternInput.deiconify()

    def browseCustomPattern(self):
        fileName = filedialog.askopenfilename(initialdir = 'C:\\')
        result = self.checkCustomPatternName(fileName)
        if(result == 1):
            self.customPatternFileList.append(fileName)

            index = self.customI
            self.customPatternLabels.append(ttk.Label(self.windowPatternInput,text=fileName, width =40))
            self.customPatternDeleteButton.append( tk.Button(self.windowPatternInput, text= 'delete', height = 1,
                           width = 8,font =self.helv18, command = lambda: self.deleteCustomPattern(index) ))
            self.customPatternLabels[-1].grid(padx = 50, pady = 10, row = self.customI, column = 0)
            self.customPatternDeleteButton[-1].grid(padx = 10, pady = 10, row = self.customI, column = 1)
            self.customI = self.customI + 1
            self.browseButton.grid(padx = 1, pady = 10, row = self.customI, column = 0, sticky = tk.S + tk.E)
            self.customQuitButton.grid(padx = 1, pady = 10, row = self.customI, column = 1, sticky = tk.S + tk.E)
            self.windowPatternInput.focus_force()
            return 1

        elif result == 2:
            MessageBoxFail = MessageBox.Mbox
            MessageBoxFail.root = root
            MessageBoxFail('The File Has Been Added!')
            self.windowPatternInput.focus_force()

        else:
            if fileName !='':
                MessageBoxFail = MessageBox.Mbox
                MessageBoxFail.root = root
                MessageBoxFail('Incorrect File Name!')
            self.windowPatternInput.focus_force()

    def createListBoxWidgets(self):
        self.horizontalScrollBar1 = tk.Scrollbar(root, orient=tk.HORIZONTAL,
                                             command = self.listBox.xview)
        self.verticalScrollBar1 = tk.Scrollbar(root, orient = tk.VERTICAL,command = self.listBox.yview )
        labelTitle = ttk.Label(root, text = 'All files you have selected:', anchor = tk.NW, width = 50)
        labelTitle.grid(sticky = tk.NW , row = 0,padx = 5, pady =1)
        self.listBox.grid(sticky = tk.N+tk.S, row = 2, column =0, columnspan =3)
        self.listBox.bind('<Button-3>', lambda event:rClick.rClicker_ListBox(event,self.fileList,root), add='')
        self.verticalScrollBar1.grid( row =2,column =3, sticky = tk.N+tk.S +tk.E)
        self.horizontalScrollBar1.grid(row =3, column= 0, columnspan =3, sticky= tk.W +tk.E +tk.S, pady =1)


        self.listBox.config(xscrollcommand = self.horizontalScrollBar1.set)
        self.listBox.config(yscrollcommand = self.verticalScrollBar1.set)

    def createResultListBoxWidgets(self):
        self.horizontalScrollBar1 = tk.Scrollbar(root, orient=tk.HORIZONTAL,
                                             command = self.resultListBox.xview)
        self.verticalScrollBar1 = tk.Scrollbar(root, orient = tk.VERTICAL,command = self.resultListBox.yview )
        labelTitle = ttk.Label(root, text = 'Analysis Result:', anchor = tk.NW, width = 50)
        labelTitle.grid(sticky = tk.NW , row = 11,padx = 5, pady =1)
        self.resultListBox.grid(sticky = tk.N+tk.S, row = 12, column =0, columnspan =3)
        self.resultListBox.bind('<Button-3>', lambda event:rClick2.rClicker2_ListBox(event,root), add='')

        self.verticalScrollBar1.grid( row =12,column =3, sticky = tk.N+tk.S +tk.E)
        self.horizontalScrollBar1.grid(row =13, column= 0, columnspan =3, sticky= tk.W +tk.E +tk.S, pady =1)


        self.resultListBox.config(xscrollcommand = self.horizontalScrollBar1.set)
        self.resultListBox.config(yscrollcommand = self.verticalScrollBar1.set)

    def createMenu(self):
        root.config(menu = self.menuBar)
        subMenu = tk.Menu(self.menuBar,tearoff=0)
        self.menuBar.add_cascade(label="File", menu=subMenu)
        #subMenu.add_command(label='New')
        #subMenu.add_separator()
        subMenu.add_command(label="Exit",command=self._quit)
        subMenuAbout = tk.Menu(self.menuBar, tearoff =0)
        subMenuAbout.add_command(label = "About", command = self.About)
        self.menuBar.add_cascade(label= "Help", menu=subMenuAbout)


    def createPatternSelectionWindowWidgets(self):
        self.openSelectionWindowButton.grid(row =10, column =0, padx =5,pady=15)
        self.openSelectionWindowButton.config(command = self.createSelectionWindow)


    def printValues(self):
        for name, var in self.singleFilePatternChoicesMap.items():
            print ("%s: %s" % (name, var.get()))

    def printValues1(self):
        for name, var in self.multiFilesPatternChoicesMap.items():
            print ("%s: %s" % (name, var.get()))


    def createAddFileWidgets(self):
        self.addFileButton.config(command = self.addFile)
        self.addFileButton.grid( row = 4, column = 0, columnspan =1,padx = 20, pady = 3)


    #create fold browser
    def createBrowseFolderWidgets(self):
        LabelBrowseFolder = ttk.Label(root, text = 'Select Output Folder (Default: .\\result):'  )
        LabelSpace = ttk.Label(root, text ="                             "  )
        LabelSpace.grid(sticky = tk.W, row =5,  column =0, padx =5, pady= 10)
        LabelBrowseFolder.grid(row =6, rowspan = 1, column =0, padx =5)
        self.textFilePath.grid( row =7, column =0, padx= 5)
        self.browseButton.grid( row =8, column =0, padx =20)
        LabelSpace2 = ttk.Label(root, text ="                             "  )
        LabelSpace2.grid(sticky = tk.W, row =9,  column =0, padx =5, pady= 5)
        self.browseButton.config(command = self.browseFolder)
        self.textFilePath.config(state=NORMAL)

    def createAnalyzeButton(self):
        self.analyzeButton.grid(row = 10, column = 1, columnspan = 3 )
        self.analyzeButton.config(command = self.analyseCsvFiles )

    def About(self):
        return 1

    #create a menu for pattern selection    
    def createPatternSelectionWidgets(self):
        self.menubutton.grid( row =10,  column =0, padx =5, pady =15 )
        self.menubutton.configure(menu=self.menuSelection)
        #self.menubutton.bind('<ButtonPress-1>',)

        for choice in self.singleFilepatternChoices:
            self.singleFilepatternChoicesMap[choice] = tk.IntVar(value = 0)
            self.menuSelection.add_checkbutton(label=choice, variable=self.singleFilepatternChoicesMap[choice],
                                 onvalue=1, offvalue=0,
                                 command=self.printValues)
            
            
    
            
        
def main():   
    app = Application(root) 
    app.master.title('CSV parse utility') 
    app.mainloop()
    
     
if __name__ == '__main__':
    main()
