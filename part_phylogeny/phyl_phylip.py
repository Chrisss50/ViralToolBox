#! /usr/bin/python
import sys
import phyl_functions
import os



if __name__ == '__main__':
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    phyl_functions.checkargs(sys.argv,err,label)
    phyl_functions.checkphylip(err,label)
    phyl_functions.runphylogeny(err,label)
    phyl_functions.mpconsense(err,label)
    phyl_functions.getconsensus(err,label)
    phyl_functions.drawtrees(err,label)

