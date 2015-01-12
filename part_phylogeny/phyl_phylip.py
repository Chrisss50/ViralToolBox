#! /usr/bin/python
import sys
import phyl_functions
import os

args = sys.argv

def main():
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    print "Checking parameters"
    phyl_functions.checkargs(args,err)
    print "Checking phylip is installed"
    phyl_functions.checkphylip(err)
    print "Running phylip"
    phyl_functions.runphylogeny(err)

if __name__ == '__main__':
    main()
