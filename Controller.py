__author__ = 'Brendan'

import sys, getopt
from Model import stats, process

def main(argv):
	stat = stats()
	#int array saying which pids have already been made
	pages = []
	#Model.process array, tuple of the format [pid, pcb]
	pcb = []
	with open(argv[0], 'r') as inputfile:
		for line in inputfile:
			#Process ID
			pid = line.split(":")[0][1]
			#Requested Page
			page = int(line.split(":")[1].strip(), 2)
			if(pid in pages):
				#This is the index of the tuple that contains the 
				#pcb corresponding to the pid
				a = [x[0] for x in pcb].index(pid)
				b = pcb[a][1].add(page)
			else:
				pcb.append((pid, process(pid)))
				pages.append(pid)
				print(pcb)
				print(pages)

if __name__ == '__main__':
	main(sys.argv[1:])
