__author__ = 'Brendan'

import sys, getopt

def main(argv):
	with open(argv[0], 'r') as inputfile:
		for line in inputfile:
			

			print line.split(":")[0][1]
			print int(line.split(":")[1].strip(), 2)

if __name__ == '__main__':
	main(sys.argv[1:])
