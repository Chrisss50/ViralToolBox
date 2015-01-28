# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 11:40:41 2014

@author: Maximilian Hanussek
"""

import os
import sys
import fnmatch
from scipy.misc import imread,imsave
from numpy import zeros
import numpy as np


# Search by name for a file in a directory
def findFileByName(path, name):
    error = []
    if(checkDirExists(path) is False):
        error.append("The file doesn't exist")
        return error
    elif(checkFileExists(path + name) is False):
        error.append("The file doesn't exist")
        return error
    else:
        result = []
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        return result


# Search by pattern for a file in a directory
def findFileByPattern(path, pattern):
    error = []
    if(checkDirExists(path) is False):
        error.append("The file doesn't exist")
        return error
    else:
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result


# Search by keyword for a line in an outputfile
def findLineByKeyword(path, keyword):
    error = []
    if(path == "The file doesn't exist"):
        error.append(str(keyword) + " couldn't be found")
        return error
    else:
        result = []
        f = open(path, 'r')
        for line in f.xreadlines():
            if keyword in line:
                result.append(line)  # without "\n"
            if keyword not in line:
                continue
        f.close()
        return result


# Search by keyword for a line in an outputfile and get the next line
def findNextLineByKeyword(path, keyword):
    error = []
    if(path == "The file doesn't exist"):
        error.append(str(keyword) + " couldn't be found")
        return error
    else:
        result = []
        with open(path, 'r+') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if keyword in line:
                    if(i+1 < len(lines)):
                        if(lines[i+1][-1:] == "\n"):
                            result.append(lines[i+1][:-1])  # without "\n"
                        else:
                            result.append(lines[i+1])
                if keyword not in line:
                    continue
        f.close
        return result


def findNext2LinesByKeyword(path, keyword):
    error = []
    if(path == "The file doesn't exist"):
        error.append(str(keyword) + " couldn't be found")
        return error
    else:
        result = []
        with open(path, 'r+') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if keyword in line:
                    if(i+2 < len(lines)):
                        if(lines[i+1][-1:] == "\n"):
                            result.append(lines[i+1][:-1])  # without "\n"
                        else:
                            result.append(lines[i+1])
                        if(lines[i+2][-1:] == "\n"):
                            result.append(lines[i+2][:-1])  # without "\n")
                        else:
                            result.append(lines[i+2])
                if keyword not in line:
                    continue
        f.close
        return result


def findNext4LinesByKeyword(path, keyword):
    error = []
    if(path == "The file doesn't exist"):
        error.append(str(keyword) + " couldn't be found")
        return error
    else:
        result = []
        with open(path, 'r+') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if keyword in line:
                    if(i+4 < len(lines)):
                        if(lines[i+1][-1:] == "\n"):
                            result.append(lines[i+1][:-1])  # without "\n"
                        else:
                            result.append(lines[i+1])
                        if(lines[i+2][-1:] == "\n"):
                            result.append(lines[i+2][:-1])  # without "\n")
                        else:
                            result.append(lines[i+3])
                        if(lines[i+2][-1:] == "\n"):
                            result.append(lines[i+3][:-1])  # without "\n")
                        else:
                            result.append(lines[i+4])
                        if(lines[i+2][-1:] == "\n"):
                            result.append(lines[i+4][:-1])  # without "\n")
                        else:
                            result.append(lines[i+4])
                if keyword not in line:
                    continue
        f.close
        return result


# Read in a file
def readInFile(path):
    error = []
    if(path == "The file doesn't exist"):
        error.append("The file doesn't exist")
        return error
    else:
        result = []
        with open(path, 'r+') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                result.append(line[:-1])
        return result


# Check if directory exists
def checkDirExists(path):
    return os.path.isdir(path)


# Check if file exists
def checkFileExists(path):
    return os.path.isfile(path)


# Check if file is empty
def checkEmptyFile(path):
    return os.path.getsize(path) > 0


# Caculate the sum of numbers given as strings
def sumUpStringList(stringList):
    numlist = map(int, stringList)
    result = sum(numlist)
    return result


# Generate a dummy picture
def generateDummyPic(resultpath):
    img = np.zeros([100, 100, 3], dtype=np.uint8)
    img.fill(255)
    imsave(resultpath + "dummy.jpg", img)
    return (resultpath + "dummy.jpg")


# Check wether an Image exists
def checkImg(path, resultpath):
    if(path == "The file doesn't exist"):
        generateDummyPic(resultpath)
        return
    else:
        return path
