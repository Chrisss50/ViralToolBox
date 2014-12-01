###################################################
#
# A short example how one can use os.pipe()
# for exchange process information petween
# parent and child process.
#
###################################################

import os
import sys


def module(err):
        print("Settings: Using Zucker algorithm for RNA structure pred.")
        err.write("Computing done, now rendering the picture")
        err.close()
        print "Module finsihed succesfully"


def main():
    # file descriptors r, w for reading and writing
    r, err = os.pipe()

    processid = os.fork()
    if processid:
        # This is the parent process
        # Closes file descriptor w
        os.close(err)
        r = os.fdopen(r)
        print "Calculating secondary rna structure..."
        str = r.read()
        print "Structure is =", str
        sys.exit(0)
    else:
        # This is the child process
        os.close(r)
        err = os.fdopen(err, 'w')
        module(err)
        sys.exit(0)

main()
