#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 20161213

@author: g00377630
'''

import os
import MessageBox
import fourfn
import xlrd
import xlwt
import re
from os import walk
import threading
import xlwtCustomStyle
#from openpyxl.reader.excel import load_workbook
import csv
import tkinter
import time
from tkinter import *
from fileinput import filename
patternFunctionMap = {}
functionList =[]

singlePatternDict = {}


#Excel file location
#directory = os.path.dirname(os.path.abspath(__file__))
directory = '.\\.\\'
singlePatternPath =   directory + 'patternLib\\'
filenamePattern = re.compile('^(?!~).+\.(xls|xlsx|xlsm|xlsb)$')
multiPatternPath = directory + 'multiPatternLib'

result=[]
'''Initialize output format '''
#styleItemName for the compared column name 
styleItemName = xlwt.easyxf('font: name Times New Roman, height 300 , color-index yellow, bold off;'
    )
styleItemName.alignment.wrap = 1
#Style0 is for normal cell
style0 = xlwt.easyxf('font: name Times New Roman, height 300 , color-index black, bold off;'
                     
    )

#styleRed is for incorrect cell: read background color and bold
#styleRed = xlwt.easyxf('font: name Times New Roman, height 280 , color-index red, bold on' )
styleRed = xlwtCustomStyle.customStyle[44]
#styleInconsistent is for the first Cell: all inconsistent item
font = xlwt.Font() 
font.name = 'Times New Roman'
font.height = 220
font.bold = True

styleInconsistent = xlwt.XFStyle()
styleInconsistent.alignment.wrap = 1
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

''' Initialize Enum pattern '''
ENUMPATTERN = {}
ENUMPATTERN_34 = {}
ENUMPATTERN_35 = {}
ENUMPATTERN_34['Dlsch_Curt_Csv_T034_聚集级别CCE_Num'] = ['LVL_1','LVL_2', 'LVL_4', 'LVL_8', 'LVL_8', 'LVL_16', 'LVL_BUTT']
ENUMPATTERN_34['Dlsch_Curt_Csv_T034_AckMode'] = ['Bundling','MultiPlexing', 'Normal']

ENUMPATTERN_35['Dest_T035_TTI_TYPE_EPDCCH_FULL_ECCE上下行配比'] = ['1_2','1_1', '2_1', '3_1', '4_1', '5_1', '7_1', '8_1', '9_1', '10_1', 'CCERATIO_BUTT']
ENUMPATTERN_35['Dest_T035_TTI_TYPE_EPDCCH_FULL_小区级ePDCCH聚集级别'] = ['LVL_1','LVL_2', 'LVL_4', 'LVL_8', 'LVL_8', 'LVL_16', 'LVL_BUTT']  
ENUMPATTERN_35['Dest_T035_TTI_TYPE_EPDCCH_FULL_Direction'] = ['LVL_1','LVL_2', 'LVL_4', 'LVL_8', 'LVL_8', 'LVL_16', 'LVL_BUTT']  
ENUMPATTERN_35['Dest_T035_TTI_TYPE_EPDCCH_FULL_ePDCCHType'] = ['COMM_SPACE','DEDI1ST_SPACE', 'DEDI2ND_SPACE', 'SPACE_BUTT']  


ENUMPATTERN['Dlsch_Curt_Csv_T034'] = ENUMPATTERN_34
ENUMPATTERN['Dest_T035_TTI_TYPE_EPDCCH_FULL'] = ENUMPATTERN_35

'''end of initialization of Enum Pattern'''


''' Initialize Calculation pattern '''
CALCPATTERN = {}
CALCPATTERN_34 = []
CALCPATTERN_35 = []
#CALCPATTERN_34['Dlsch_Curt_Csv_T034_小区TBS配额'] = ['Yk']
#CALCPATTERN_35['Dest_T035_TTI_TYPE_EPDCCH_FULL_DCI1_Dcilen'] = ['DCI1_StartCCENo', 'DCI1_NumCCE']

CALCPATTERN['Dlsch_Curt_Csv_T034'] = CALCPATTERN_34
CALCPATTERN['Dest_T035_TTI_TYPE_EPDCCH_FULL'] = CALCPATTERN_35

'''end of initialization of Calculation Pattern'''

'''BEGINNING OF CUSTOM PATTERN SERIAL NUMBER<->NAME MAP'''
SERNUM_FILENAME_MAP= {}
SERNUM_FILENAME_MAP[32] = 'Dest_T032_TTI_TYPE_DLSCH_BASE'
SERNUM_FILENAME_MAP[34] = 'Dlsch_Curt_Csv_T034'
SERNUM_FILENAME_MAP[35] = 'Dest_T035_TTI_TYPE_EPDCCH_FULL'
SERNUM_FILENAME_MAP[44] = 'Dest_T044_TTI_TYPE_DLSCH_CELL_CAP_TIME'
SERNUM_FILENAME_MAP[52] = 'Dest_T052_TTI_TYPE_EPDCCH_ECCERES_RES'
SERNUM_FILENAME_MAP[117] = 'Dest_T117_COMM_TTI_L2L1_PDSCH'

'''END OF CUSTOM PATTERN SERIAL NUMBER<->NAME MAP'''


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
    
    




def checkFileName(fileName):
        if os.path.isfile(singlePatternPath + fileName) == 0:
            return 0
        else :
            match = filenamePattern.match(fileName)
            if match:
                return 1
            else:
                return 0

'''
Read the rules in Excel
'''
def readSinglePatterns(root, resultListBox):
    for filename in os.listdir(singlePatternPath):
        if(checkFileName(filename)):
            try:
                data = xlrd.open_workbook(singlePatternPath + filename)
                table = data.sheets()[0]
                ncols = table.ncols
                row0 = table.row_values(0)
                row1 = table.row_values(1)
                pattern ={}
                for i in range(0,ncols):
                    pattern[row0[i]] = row1[i]
                fileNameKey = filename.split('.',1)[0]
                singlePatternDict[fileNameKey] = pattern
                #MessageBoxPromt(0, 'Exception' + '\n  good', root )
                resultListBox.insert(END, 'Successfully read pattern ' + filename + '!')
            except Exception as e:
                MessageBoxPromt(0, 'Exception '  + str(e) + '\n  ERROR 1 in reading pattern file', root )
                resultListBox.insert(END, 'Failed to  read pattern ' + filename + '! Exception: ' + str(e))
                print (e)
                return 0
    return 1
    #print singlePatternDict['Dest_T035_TTI_TYPE_EPDCCH_FULL']
   

def transformToFloat(s):
    try:
        return float(s)
    except ValueError:
        return s
'''
Todo: Specify the rules for choice like Enum

'''

def compareItemDirectly(key, pattern, item ):
    if(transformToFloat(pattern[key]) == transformToFloat(item)):
        return 1
    else:
        return 0
      
def compareEnumItem(item, pN, enumItemName, key, pattern):
    enumList = ENUMPATTERN[pN][enumItemName]
    if pattern[key] == 'ENUMALLCASES':
        for enumItem in enumList:
            if transformToFloat(enumItem) == transformToFloat(item):
                return 1
    else:
        patternList = pattern[key].split(',')
        for enumItem in patternList:
            if transformToFloat(enumItem) == transformToFloat(item):
                return 1
    return 0  


def compareCalcItem(item, pN, calcItemName, key, pattern):
    calcList = CALCPATTERN[pN][calcItemName]
    if (calcItemName == 'Dlsch_Curt_Csv_T034_小区TBS配额'):
        return 0
    elif (calcItemName == 'Dest_T035_TTI_TYPE_EPDCCH_FULL_DCI1_Dcilen'):
        return 0
    
'''
core function
compare the custom pattern line by line
1. using fourfn to compare
2. 
'''
def compareCustomPattern(patternName, customPattern, reader, root, resultListBox, prgBox, destinationFolderName, total2, fileName):  
    data = list(reader)
    rowCount = len(data)
    print ('rowCount = ', rowCount) 
    print ('Compare Mode is:\n', customPattern, '\nThe result of pattern: ', patternName, 'is\n ')
    fourfn.exprStack = []
    results = fourfn.BNF().parseString(customPattern) 
    print('fourfn.exprStack', fourfn.exprStack)
    #print (fourfn.exprStack)
    exprStackTemp = fourfn.exprStack[:]
    sa = fourfn.SpecificAnalyser(data, exprStackTemp)
    resultNameLine, resultMatrix, inconsistentItemMatrix, inconsistentLineNumber = sa.analyzeCsv(resultListBox, customPattern)
    prgBox.progressBar['value'] = prgBox.progressBar['value'] + total2/2     
    try:
        #print ('size of inconsistentItemMatrix\n', inconsistentItemMatrix )
        #print ('size of resultMatrix\n', resultMatrix )
        exportToFile(resultNameLine, resultMatrix, inconsistentItemMatrix, patternName, prgBox, total2, destinationFolderName, inconsistentLineNumber, fileName, exprStackTemp)
        resultListBox.insert(END, 'Successfully Exported Result! ' + patternName )
        print ( prgBox.progressBar['value'])
    except Exception as e:
        print ('Exception ' + str(e))
        print ('Error 51 in writing result(.xls) files')
        resultListBox.insert(END, 'Error 51 in writing result(.xls) files! Exception: '+ str(e))
        MessageBoxPromt(1, 'Exception ' + str(e), root, prgBox )
    
    return 0     
'''
core function 
compare the value between csv files and rules
'' or space mean that we dont need to compare that column
'-' means basic information, we just keep them
prgBox and total is the paras for progress Bar
pN is pattern name
'''    
def compare(reader, pN, prgBox, total):
    i = 0
    itemNameList = []
    resultNameLine = []
    resultMatrix = []
    inconsistentItemMatrix = []
    #originalValue = prgBox.progressBar['value']
    #The first line is Column Name
    data = list(reader) 
    rowCount = len(data) 
    #the pattern has Enum pattern in it
    enumPatternFlag = 0
    calcPatternFlag = 0
    if(pN in ENUMPATTERN):
        enumPatternFlag = 1
    if(pN in CALCPATTERN):
        calcPatternFlag = 1
    for line in data:  
        if i == 0:
            i = i + 1
            itemNameList = line
            continue
        else:
            pattern = singlePatternDict[pN]
            itemNumber = 0
            resultLine = []
            inconsistentItemLine = []
            for item in line:
                specialItemName = ''
                specialKeyFlag = 0  
                try:
                    key = itemNameList[itemNumber]
                except:
                    continue
                #print (key)
                itemNumber = itemNumber + 1
                if pattern[key] == '' or  pattern[key] == ' ':
                    continue
                
                elif pattern[key] == '-' :
                    if i == 1:
                        resultNameLine.append(key)
                    resultLine.append(item)
                    
                else:
                    if i == 1:
                        resultNameLine.append(key)
                    ''' core of comparison'''    
                    ''' Add more pattern here '''    
                    specialItemName = (pN+'_'+key)
                    if(enumPatternFlag == 0 and calcPatternFlag == 0): 
                        specialKeyFlag = 0
                    elif(enumPatternFlag == 1 and specialItemName in ENUMPATTERN[pN]):
                        specialKeyFlag = 1 
                    elif(calcPatternFlag == 1 and specialItemName in CALCPATTERN[pN]):
                        specialKeyFlag = 2
                        
                    if(specialKeyFlag == 0):
                        if(compareItemDirectly(key, pattern, item)):
                            resultLine.append('Correct')
                        else:
                            resultLine.append('Incorrect')
                            inconsistentItemLine.append(key)
                    elif(specialKeyFlag == 1):
                        if(compareEnumItem(item, pN, specialItemName, key, pattern)):
                            resultLine.append('Correct')
                        else:
                            resultLine.append('Incorrect')
                            inconsistentItemLine.append(key)
                    elif(specialKeyFlag == 2):
                        if(compareCalcItem(item, pN, specialItemName, key, pattern)):
                            resultLine.append('Correct')
                        else:
                            resultLine.append('Incorrect')
                            inconsistentItemLine.append(key)
            i = i + 1
            resultMatrix.append(resultLine)    
            inconsistentItemMatrix.append(inconsistentItemLine)  
           
        prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(total/rowCount)/2
    return resultNameLine, resultMatrix, inconsistentItemMatrix                  
    
                        
    '''
    Export result to file 
    prgBox, total is paras for progressBox
    '''      
def analyzeCustomPattern(fileList, patternChoicesMap, customFilePatternContentMap, root, resultListBox, prgBox, destinationFolderName, total):  
    length_fileList = 0
    length_patternChoicesMap = 0
    if (len(fileList) == 0 ):
        length_fileList = 1
    else:
        length_fileList = len(fileList)
    if (len(patternChoicesMap.keys()) == 0):
        length_patternChoicesMap = 1
    else:
        length_patternChoicesMap = len(patternChoicesMap.keys())
    
    progressProceeding = float(total/(length_fileList * length_patternChoicesMap))/2          
    total2 = float(total/2)
    
    for fileName in fileList:
            patternNameTemp = fileName.split('_0_0_0x',1)[0]
            if patternNameTemp == fileName:
                #prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(90/len(fileList))/2
                continue
            else:
                patternName =  patternNameTemp.split('\\')[-1]
                #prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(5/len(fileList))/2
            '''patternChoicesMap is not empty'''
            for customPatternFile in patternChoicesMap.keys():
                if patternChoicesMap[customPatternFile].get() == 2:
                    '''Analyse Input File'''
                    patternDict = customFilePatternContentMap[customPatternFile]
                    pureCustomPatternFileName = customPatternFile.split('/')[-1].split('.')[0]
                    for pattern in patternDict.keys():
                        try:
                            if SERNUM_FILENAME_MAP[pattern] == patternName:
                                #open the file and do analysis
                                customPattern = patternDict[pattern]
                                with open(fileName, 'r') as f:
                                    reader = csv.reader(f) 
                                    compareCustomPattern(patternName, customPattern,reader, root, resultListBox, prgBox, destinationFolderName, total2, pureCustomPatternFileName)
                            prgBox.progressBar['value'] = prgBox.progressBar['value'] + progressProceeding
                            resultListBox.insert(END, 'Parsing Custom Pattern :' + customPatternFile + ' OK!');
                        except IndexError:
                            print ('Error 52: Exception: IndexError')
                            resultListBox.insert(END, 'Error 52 in Compare Custom Pattern! Exception: IndexError')
                            MessageBoxPromt(1, 'Exception: IndexError', root, prgBox )
                            prgBox.progressBar['value'] = prgBox.progressBar['value'] + progressProceeding
                            continue
                    
                else:
                    prgBox.progressBar['value'] = prgBox.progressBar['value'] + progressProceeding
                        
def exportToFile(resultNameLine, resultMatrix, inconsistentItemMatrix, patternName, prgBox, total, exportDir = None,inconsistentLineNumber = None, fileName = None, exprStackTemp = None):
    wbook = xlwt.Workbook()
    wsheet = wbook.add_sheet(patternName[:31],cell_overwrite_ok=True)
    indexRow = 1 
    indexColumn = 0
    realInconsistentItemMatrix = []
    realINconsistentItemCount = []
    binaryTreeKeyDataMapList = []
    #if exprStackTemp is None then it's normal mode
    if exprStackTemp is  None:
        for item in inconsistentItemMatrix:
            itemStr = ''
            for element in item:
                itemStr = itemStr + str(element)
                itemStr += ',\n'
            realInconsistentItemMatrix.append(itemStr)
    #else it's custom compare mode
    else:
        exprStackTemp.reverse()
        for item in inconsistentItemMatrix:
            if (exprStackTemp is None):
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + total/2     
                return
            bt = fourfn.BinaryTree(exprStackTemp, item)

            bt.convert(bt.NodeList)

            #bt.printTree_Simple()
             
            bt.traverseTree(bt.root)
            #bt.printTree_Simple()
            realInconsistentItemMatrix.append(bt.resultString)
            binaryTreeKeyDataMapList.append(bt.keyNodeData)
            realINconsistentItemCount.append(bt.totalPair)
            bt.printTree(inconsistentItemMatrix)
                
    #totalCount = 0            
    for item in realInconsistentItemMatrix:
        wsheet.write(indexRow,indexColumn, item, styleInconsistent)
       
        wsheet.col(indexColumn).width = 10000
        #totalCount = totalCount + 1
        indexRow = indexRow + 1
    #prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(total/5)
    indexRow = 0
    indexColumn = 1

    for item in resultNameLine:
        tag = 0 
        for itemsInconsistent in inconsistentItemMatrix:
            if exprStackTemp is None:
                if item in itemsInconsistent:
                    tag = 1
                    break
 
                
        if tag == 0:
            wsheet.write(indexRow,indexColumn, item, styleItemName)
            wsheet.col(indexColumn).width = 3000
        elif tag ==1:
            wsheet.write(indexRow,indexColumn, item, styleRed)
            wsheet.col(indexColumn).width = 5000        
        indexColumn = indexColumn + 1
        '''IndexColumn should be less than 256 for now'''
        if indexColumn >=256:
            break
    #prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(total/5)  
    
    indexRow = 1
    
    for item in resultMatrix:
    
        indexColumn = 1
        print ('inconsistentLineNumber' , inconsistentLineNumber )
        for element in item:
            if (inconsistentLineNumber is None):
                if(element == 'Incorrect'):
                    wsheet.write(indexRow,indexColumn, element, styleRed)
                else:
                    wsheet.write(indexRow,indexColumn, element, style0)
            else:
                if exprStackTemp is None:
                    if(indexRow in inconsistentLineNumber):
                       wsheet.write(indexRow,indexColumn, element, styleRed)
                    else:
                       wsheet.write(indexRow,indexColumn, element, style0)  
                else:
                    print ('***********************************************')
                    key = resultNameLine[indexColumn-1]
                    print (binaryTreeKeyDataMapList[indexRow-1])
                    print (key)
                    if(key in binaryTreeKeyDataMapList[indexRow-1]):
                        styleIndex =  binaryTreeKeyDataMapList[indexRow-1][key] 
                        if styleIndex > 55:
                            styleIndex = 55
                        wsheet.write(indexRow,indexColumn, element, xlwtCustomStyle.customStyle[  styleIndex    ])
                    else:
                        wsheet.write(indexRow,indexColumn, element, style0)
            #prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(3*total/(5*len(resultMatrix)*len(item)))
            '''IndexColumn should be less than 256 for now'''
            indexColumn = indexColumn + 1
            if indexColumn >=256:
                break
        indexRow = indexRow + 1
        
    newPath = directory + '\\result'
    outputFileName = ''
    if fileName == None or fileName == '':
        outputFileName = patternName
    else:
        outputFileName = patternName + '____' + fileName
    
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    if(exportDir == '' or exportDir == None):
        filepath = newPath + '\\result_'+outputFileName + '.xls'
        print (filepath)
        wbook.save(filepath)
    else:
        print (exportDir)
        wbook.save(exportDir + '\\result_'+outputFileName + '.xls')
    prgBox.progressBar['value'] = prgBox.progressBar['value'] + total/2       

    
    
    
'''
compareMode = 0 : Single file compare. For each file in the fileList, there is a corresponding pattern. If the pattern exists, we analyze the file.

prgBar allocate: 5, 5, 15, 60, 5 total = 90
'''

def Analyse(fileList,customFilePatternContentMap, patternChoicesMap, destinationFolderName, root, resultListBox, prgBox):
   
    statusFlag = 1;
    ErrorInformation = []
   
    if (readSinglePatterns(root, resultListBox)== 1):
        prgBox.progressBar['value'] = 10
        resultListBox.insert(END, 'Successfully read all patterns! ')
    else:
        resultListBox.insert(END,'Error 1 in reading pattern files')
        ErrorInformation.append('Error 1 in reading pattern files')
        print(ErrorInformation)
        prgBox.quit()
        MessageBoxPromt(1, 'Error 1 in reading pattern files!', root, prgBox, prgBoxValue = 100 )
        return 0, ErrorInformation
    
    sheetIndex = 0
    if(os.path.isdir(destinationFolderName) == 0 and destinationFolderName !=''):
        resultListBox.insert(END, 'The output folder is INVALID!')
        MessageBoxPromt(1, 'The output folder is INVALID!', root, prgBox )
        return 0
    else:
        for fileName in fileList:
            patternNameTemp = fileName.split('_0_0_0x',1)[0]
            if patternNameTemp == fileName:
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(90/len(fileList))/2
                continue
            else:
                patternName =  patternNameTemp.split('\\')[-1]
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(5/len(fileList))/2
                try:
                    if(patternChoicesMap ==  {} ):
                        statusFlag = 0
                        resultListBox.insert(END, 'Please Select One Pattern')
                        MessageBoxPromt(1, 'Please Select One Pattern', root, prgBox )
                        return statusFlag, ErrorInformation
                    if(patternName in singlePatternDict.keys() and patternChoicesMap[patternName].get() == 1):
                    #if(patternName in singlePatternDict.keys() and patternChoicesMap[patternName]== 1 ):
                        with open(fileName, 'r') as f:
                            reader = csv.reader(f) 
                            prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(5/len(fileList))/2             
                            try:                  
                                resultNameLine, resultMatrix, inconsistentItemMatrix = compare(reader, patternName, prgBox, float(16/len(fileList)))
                                resultListBox.insert(END, 'Successfully Compared ' + patternName)
                                print ( prgBox.progressBar['value'])
                            except Exception as e:
                                statusFlag = 0
                                ErrorInformation.append(str(e))  
                                print('Exception ' + str(e))
                                print ('ERROR 2  in comparison!')
                                resultListBox.insert(END, 'Error 2 in Comparison! Exception: ' + str(e))
                                MessageBoxPromt(1, 'Exception ' + str(e), root, prgBox )
                                prgBox.quit() 
                                
                            try:
                                exportToFile(resultNameLine, resultMatrix, inconsistentItemMatrix, patternName,  
                                             prgBox, float(64/len(fileList)), destinationFolderName )
                                resultListBox.insert(END, 'Successfully Exported Result! ' + patternName )
                                print ( prgBox.progressBar['value'])
                            except Exception as e:
                                print ('Exception ' + str(e))
                                print ('Error 3 in writing result(.xls) files')
                                statusFlag = 0
                                ErrorInformation.append(str(e))
                                resultListBox.insert(END, 'Error 3 in writing result(.xls) files! Exception: '+ str(e))
                                MessageBoxPromt(1, 'Exception ' + str(e), root, prgBox )
                            sheetIndex = sheetIndex + 1
                    
                    else:#no such pattern for this file
                        prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(85/len(fileList))/2
                        Error = 'Failed to compare file: ' + fileName + ' (Regular Pattern is not Found or Selected!)'
                        resultListBox.insert(END, Error)
                        ErrorInformation.append(Error)
                        continue
                except Exception as e:
                    print ('Exception ' + str(e))
                    print ('Error 4 in reading source csv files')  
                    MessageBoxPromt(0, 'Exception ' + str(e), root, prgBox ) 
                    resultListBox.insert(END, 'Error 4 in reading source csv files! Exception: ' + str(e))
                    ErrorInformation.append(str(e)) 
                    statusFlag = 0; 
                    
        '''Analyze In Custom Compare Mode'''
        total = 100 - prgBox.progressBar['value']
        analyzeCustomPattern(fileList, patternChoicesMap, customFilePatternContentMap, root, resultListBox, prgBox, destinationFolderName, total)  
    prgBox.progressBar['value'] = 100            
    time.sleep(0.4)               
    prgBox.quit()
    return statusFlag, ErrorInformation
    

def AnalyseMultiThreads(fileList, patternChoicesMap, destinationFolderName, root, resultListBox, prgBox):    
    statusFlag = 1;
    ErrorInformation = []
   
    if (readSinglePatterns(root, resultListBox)== 1):
        prgBox.progressBar['value'] = 10
        resultListBox.insert(END, 'Successfully read all patterns! ')
    else:
        resultListBox.insert(END,'Error 1 in reading pattern files')
        ErrorInformation.append('Error 1 in reading pattern files')
        print(ErrorInformation)
        prgBox.quit()
        MessageBoxPromt(1, 'Error 1 in reading pattern files!', root, prgBox, prgBoxValue = 100 )
        return 0, ErrorInformation
    
    sheetIndex = 0
    if(os.path.isdir(destinationFolderName) == 0 and destinationFolderName !=''):
        resultListBox.insert(END, 'The output folder is INVALID!')
        MessageBoxPromt(1, 'The output folder is INVALID!', root, prgBox )
        return 0
    else:
        '''Analyze In Normal Compare Mode'''
        for fileName in fileList:
            patternNameTemp = fileName.split('_0_0_0x',1)[0]
            if patternNameTemp == fileName:
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(90/len(fileList))
                continue
            else:
                patternName =  patternNameTemp.split('\\')[-1]
   
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(5/len(fileList))
                try:
                    if(patternChoicesMap ==  {} ):
                        statusFlag = 0
                        resultListBox.insert(END, 'Please Select One Pattern')
                        MessageBoxPromt(1, 'Please Select One Pattern', root, prgBox )
                        return statusFlag, ErrorInformation
                    if(patternName in singlePatternDict.keys()):
                    #if(patternName in singlePatternDict.keys() and patternChoicesMap[patternName]== 1 ):
                        with open(fileName, 'r') as f:
                            reader = csv.reader(f) 
                            prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(5/len(fileList))             
                            try:                  
                                resultNameLine, resultMatrix, inconsistentItemMatrix = compare(reader, patternName, prgBox, float(16/len(fileList)))
                                resultListBox.insert(END, 'Successfully Compared ' + patternName)
                                print ( prgBox.progressBar['value'])
                            except Exception as e:
                                statusFlag = 0
                                ErrorInformation.append(str(e))  
                                print('Exception ' + str(e))
                                print ('ERROR 2  in comparison!')
                                resultListBox.insert(END, 'Error 2 in Comparison! Exception: ' + str(e))
                                MessageBoxPromt(1, 'Exception ' + str(e), root, prgBox )
                                prgBox.quit() 
                                
                            try:
                                exportToFile(resultNameLine, resultMatrix, inconsistentItemMatrix, patternName,  
                                             prgBox, float(64/len(fileList)), destinationFolderName )
                                resultListBox.insert(END, 'Successfully Exported Result! ' + patternName )
                                print ( prgBox.progressBar['value'])
                            except Exception as e:
                                print ('Exception ' + str(e))
                                print ('Error 3 in writing result(.xls) files')
                                statusFlag = 0
                                ErrorInformation.append(str(e))
                                resultListBox.insert(END, 'Error 3 in writing result(.xls) files! Exception: '+ str(e))
                                MessageBoxPromt(1, 'Exception ' + str(e), root, prgBox )
                            sheetIndex = sheetIndex + 1
                    else:#no such pattern for this file
                        prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(85/len(fileList))
                        Error = 'Failed to compare file: ' + fileName + ' (Pattern is not Found or Selected!)'
                        resultListBox.insert(END, Error)
                        ErrorInformation.append(Error)
                        continue
                except Exception as e:
                    print ('Exception ' + str(e))
                    print ('Error 4 in reading source csv files')  
                    MessageBoxPromt(0, 'Exception ' + str(e), root, prgBox ) 
                    resultListBox.insert(END, 'Error 4 in reading source csv files! Exception: ' + str(e))
                    ErrorInformation.append(str(e)) 
                    statusFlag = 0; 
     
    time.sleep(0.3)               
    #prgBox.quit()
    return statusFlag, ErrorInformation


def AnalyseSchedulingNotEnough(fileList, destinationFolderName, root, resultListBox,prgBox):
    statusFlag = 1;
    ErrorInformation = []

    sheetIndex = 0
    if (os.path.isdir(destinationFolderName) == 0 and destinationFolderName != ''):
        resultListBox.insert(END, 'The output folder is INVALID!')
        MessageBoxPromt(1, 'The output folder is INVALID!', root, prgBox)
        return 0
    else:
        for fileName in fileList:
            patternNameTemp = fileName.split('_0_0_0x', 1)[0]
            if patternNameTemp == fileName:
                prgBox.progressBar['value'] = prgBox.progressBar['value'] + float(90 / len(fileList)) / 2
                continue
            else:

    return 1

'''
def main():   
    fileList = ['D:\\python workspace\\CsvReader\\test1\\testCsvFiles\\Dest_T035_TTI_TYPE_EPDCCH_FULL_0_0_0x60f001f.csv',
                'C:\\Users\\g00377630\\Desktop\\python3.4\\testCsvFiles\\Dest_T052_TTI_TYPE_EPDCCH_ECCERES_RES_0_0_0x60f001f.csv',
                'D:\\python workspace\\CsvReader\\test1\\testCsvFiles\\Dlsch_Curt_Csv_T034_0_0_0x19102124.csv']
    patternChoicesMap ={
                        'Dest_T035_TTI_TYPE_EPDCCH_FULL' : 0,
                        'Dest_T052_TTI_TYPE_EPDCCH_ECCERES_RES' : 1,
                        'Dlsch_Curt_Csv_T034' : 0
                        }
    
    destinationFolderName = directory 
    root =tkinter.Tk()
    
    compareMode = 0
    #Analyse(fileList, patternChoicesMap, destinationFolderName, root, compareMode)
 
    
if __name__ == '__main__':
    main()
'''


    
