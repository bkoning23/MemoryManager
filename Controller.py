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
				#a is the index of the process in the PCB, 1
				#should be hardcoded because it is the second 
				#item in the tuple.
				pcb[a][1].add(page)
			else:
				#This is if the process has not been recorded yet
				pcb.append((pid, process(pid)))
				pages.append(pid)
			print ("Process " + str(pid) + " accessed Page " + str(page))

		for i in pcb:
			print("Process " + str(i[0]) + " referenced " + str(i[1].getrefcount()) + " times.")
			print("Process " + str(i[0]) + " size: " + str(i[1].getpagecount()) + " pages.")
			

if __name__ == '__main__':
	main(sys.argv[1:])
