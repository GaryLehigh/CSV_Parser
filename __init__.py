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
data_files = [("Microsoft.VC80.CRT", glob(r'.\\Microsoft.VC80.CRT\\*.*'))]
'''
setup(
    data_files=data_files,
    windows = [
        {
            "script": directory +"\\Draw.py",
            "icon_resources":[(1, directory + "\\myicon.ico")]
        }
    ],
    
  )

'''
setup(
    data_files=data_files,
    console = [
        {
            "script": directory +"\\Draw.py",
            "icon_resources":[(1, directory + "\\myicon.ico")]
        }
    ],
    
  )
