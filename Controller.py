__author__ = 'Brendan'

import sys, getopt


def main(argv):
    inputfile = open(argv[2], 'r')
    print (inputfile)



if __name__ == '__main__':
    main(sys.argv[1:])
