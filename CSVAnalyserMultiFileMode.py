#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 

@author: g00377630
'''

'''
compareMode = 1 : Multiple files compare. For each pattern in the multi-pattern list, we compare all files in the fileList simultaneously
'''
import os
import MessageBox
import xlrd
import xlwt
import re
from os import walk
import threading
#from openpyxl.reader.excel import load_workbook
import csv
import tkinter
import time
from tkinter import *


'''Initialize output format '''
#styleItemName for the compared column name 
styleItemName = xlwt.easyxf('font: name Times New Roman, height 300 , color-index yellow, bold off;'
    )
#Style0 is for normal cell
style0 = xlwt.easyxf('font: name Times New Roman, height 200 , color-index black, bold off;'
                     
    )

#styleRed is for incorrect cell: read background color and bold
styleRed = xlwt.easyxf('font: name Times New Roman, height 280 , color-index red, bold on' )

#styleInconsistent is for the first Cell: all inconsistent item
font = xlwt.Font() 
font.name = 'Times New Roman'
font.height = 220
font.bold = True

styleInconsistent = xlwt.XFStyle()
styleInconsistent.alignment.wrap = 0
styleInconsistent.font = font

patternYellow = xlwt.Pattern()
patternYellow.pattern = xlwt.Pattern.SOLID_PATTERN
patternYellow.pattern_fore_colour = 5
styleRed.pattern = patternYellow
styleInconsistent.pattern = patternYellow
styleInconsistent.font = font

pattern2 = xlwt.Pattern()
pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
pattern2.pattern_fore_colour = 4
styleItemName.pattern = pattern2
''' end of initialization of output format'''

patternFunctionMap = {}
multiPatternDict = {}
inputFiles = {} #All input data


def MessageBoxPromt(isQuit, msg, root, prgBox = None, prgBoxValue = 0 ):
    try:
        if (prgBox is not None):
            prgBox.progressBar['value'] = prgBoxValue
            if(isQuit):
                prgBox.quit()
    except Exception as e:
        print (str(e))
    MessageBoxFail = MessageBox.Mbox
    MessageBoxFail.root = root
    MessageBoxFail(msg)
    
    
def readFile(filePath, resultListBox):
    file1 = []
    fileNameTemp = filePath.split('_0_0_0x',1)[0]
    fileRealName =  fileNameTemp.split('\\')[-1]   
    try:
        with open(filePath, 'r') as f:
            reader = csv.reader(f) 
            data = list(reader) 
            for line in data:
                file1.append(line)
        inputFiles[fileRealName] = file1
        return 1
    except Exception as e:
        resultListBox.insert(END, 'Error in reading file  {' + filePath + '}  Exception: ' + str(e))
        return 0
        
            
def fileCombinationValidation(fileList, patternName, ErrorInformation, resultListBox):
    listPatternNamesRequired = multiPatternDict[patternName][:-1]
    patternListOfAllFiles = {}
    for filePath in fileList:
        fileNameTemp = filePath.split('_0_0_0x',1)[0]
        patternRealName =  fileNameTemp.split('\\')[-1]   
        #Map of pattern real name and file path     
        patternListOfAllFiles[patternRealName] = filePath
    for patternRealName in listPatternNamesRequired:
        if patternRealName in patternListOfAllFiles.keys():
            if(patternRealName not in inputFiles.keys()):
                if(readFile(filePath, resultListBox) == 0):
                    Error = 'Csv file named:  {' + filePath + '}  cannot be read!'
                    ErrorInformation.append(Error)
                    resultListBox.insert(END, Error)
                    return 0
                else:
                    #print successfully reading  message
                    resultListBox.insert(END, 'Successfully read csv file' + patternListOfAllFiles[patternRealName])
                    continue
        else:
            #print errorMessage
            Error = 'Pattern that named : ' + patternName + ' cannot be found in PatternLib!'
            ErrorInformation.append(Error)
            resultListBox.insert(END, Error)
            return 0
    #print successMessage
    return 1

'''
Compare MultiFiles, for each pattern, we have a specific handler function
'''                
def compareMultiMode(patternName, ErrorInformation, resultListBox):  
    handler = multiPatternDict[patternName][-1]
    return handler()

def Analyse(fileList, patternChoicesMap, destinationFolderName, root, resultListBox, prgBox):
    #Multi-File Mode
    statusFlag = 1;
    ErrorInformation = []
    #prgBox.progressBar['value'] = 10
    #initialize Pattern <-> Handler match 
    initPatternFunction()
    if(os.path.isdir(destinationFolderName) == 0 and destinationFolderName !=''):
        MessageBoxPromt(1, 'The output folder is INVALID!', root, prgBox)
        Error = 'Error 6 Invalid Folder Name: ' + destinationFolderName
        ErrorInformation.append(Error)
        resultListBox.insert(END, 'Error 6 Invalid Folder Name: ' + destinationFolderName)
        statusFlag = 0
        return statusFlag, ErrorInformation
    else:
        prgBox.quit()
        for patternName in patternChoicesMap.keys():
            if(patternChoicesMap[patternName].get() == 0):
                continue
            else:
                if patternName in multiPatternDict.keys():
                    try:
                        if(fileCombinationValidation(fileList, patternName, ErrorInformation, resultListBox)):
                           
                            try:
                                if(compareMultiMode(patternName, ErrorInformation, resultListBox) == 0 ):
                                    Error = 'Error 7 multi-pattern: ' + patternName + ': failed to compare csv files!'
                                    ErrorInformation.append(Error)    
                                    resultListBox.insert(END, Error)  
                                else:
                                    resultListBox.insert(END, 'Successfully analyze pattern ' + patternName + '!')      
                            except Exception as e:
                                Error = 'Exception in analyzing files for multi-pattern: ' + patternName +'! Exception: ' + str(e)
                                ErrorInformation.append(Error)
                                resultListBox.insert(END, Error)   
                              
                        else:
                            Error = 'Error 8 multi-pattern: ' + patternName + ' does not have corresponding input files!'
                            ErrorInformation.append(Error)
                            resultListBox.insert(END, Error)
                    except Exception as e:
                            Error = 'Exception in checking file combinations for multi-pattern: ' + patternName +'! Exception: ' + str(e)
                            ErrorInformation.append(Error)
                            resultListBox.insert(END, Error)

                else:
                    Error = 'Error 9 multi-pattern: ' + patternName + ' does not have handler!'
                    resultListBox.insert(END, Error)
                    statusFlag = 0
                    return statusFlag, ErrorInformation
                
                
                
                
                
                
                
def initPatternFunction():
    list_34_35_1 = ["Dlsch_Curt_Csv_T034", "Dest_T035_TTI_TYPE_EPDCCH_FULL", handler_34_35_1]
    list_34_52_1 = ["Dlsch_Curt_Csv_T034", "Dest_T052_TTI_TYPE_EPDCCH_ECCERES_RES", handler_34_52_1]
    list_custom = [handler_custom]
    multiPatternDict['34_35_1'] = list_34_35_1
    multiPatternDict['34_52_1'] = list_34_52_1
    multiPatternDict['custom']  = list_custom
    
    
        
def handler_34_35_1():
    return 1

def handler_34_52_1():
    return 0

def handler_custom():
    return 0

def function3():
    return 0

def function4():
    return 0

def function5():
    return 0

def function6():
    return 0
