# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 11:40:41 2014

@author: Maximilian Hanussek
"""


import sys
import os
import fnmatch


# Search by name for a file in a directory
def findFileByName(path, name):
    error = []
    if(checkDirExists(path) is False):  #'or checkFileExists(path) is False):
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
    if(checkDirExists(path) is False):  #or checkFileExists(path) is False):
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
    if(checkFileExists(path) is False):
        error.append("The file doesn't exist")
        return error
    else:
        result = []
        f = open(path, 'r')
        for line in f.xreadlines():
            if keyword in line:
                result.append(line[:-1])  # without "\n"
            if keyword not in line:
                continue
        f.close()
        return result


# Search by keyword for a line in an outputfile and get the next line
def findNextLineByKeyword(path, keyword):
    error = []
    if(checkFileExists(path) is False):
        error.append("The file doesn't exist")
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


# Check if directory exists
def checkDirExists(path):
    return os.path.isdir(path)


# Check if file exists
def checkFileExists(path):
    return os.path.isfile(path)


# Check if file is empty
def checkEmptyFile(path):
    return os.path.getsize(path) > 0


def sumUpStringList(stringList):
    numlist = map(int, stringList)
    result = sum(numlist)
    return result

if __name__ == "__main__":
    pathdir = sys.argv[1]
    print findFileByPattern(pathdir, "domain_graphic*")
    StringList = map(str, [1, 2, 3])
