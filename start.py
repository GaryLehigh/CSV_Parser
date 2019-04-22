#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Function:
Author:     Xiang Gao
Version:    2016-12-8
"""



from distutils.core import setup
import py2exe
import sys
import os

from glob import glob


if len(sys.argv) == 1:
    sys.argv.append("py2exe")

directory = os.path.dirname(os.path.abspath(__file__))

    
data_files = [("Microsoft.VC80.CRT", glob(r'D:\\vs\\VC\\redist\\x86\\Microsoft.VC80.CRT\\*.*'))]

setup(
    data_files=data_files,
    windows = [
        {
            "script": directory +"\\CsvReader1.py",
            "icon_resources":[(1, directory + "\\myicon.ico")]
        }
    ],
    
  )


'''
setup(
    data_files=data_files,
    windows = [".\\CsvReader1.py"  ]
    
  )
'''
