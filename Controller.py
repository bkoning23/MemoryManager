__author__ = 'Brendan'

import sys, getopt
from Model import stats, process, freeframelist, mainmemory

def main(argv):
	stat = stats()
	#int array saying which pids have already been made
	pids = []
	#Model.process array, tuple of the format [pid, pcb]. This is a collection of PCBs that the OS manages
	pcb = []
	#Free frame list
	freeframes = freeframelist(16)
	#Memory
	memory = mainmemory(16)
	with open(argv[0], 'r') as inputfile:
		for line in inputfile:
			#Process ID
			pid = line.split(":")[0][1]
			#Requested Page
			page = int(line.split(":")[1].strip(), 2)
			print ("Process " + str(pid) + " accessed Page " + str(page))
			
			#check if page is in memory
			if(memory.isinmemory(pid, page)):
				print("ITS IM MEMEORY")
			else:
				print ("NOT IN MEMORY")
				try:	
					memory.addtomemory(pid, page)
					print("adding " + str(page) + " " + str(pid))
				except mainmemory.MemError:
					print ("OUT OF MEMORY LRU REPLACE")
					memory.lru(pid, page)

			memory.topofstack(pid, page)
			print(memory.getstack())
				

			#if(freeframes.isempty()):
				#print(freeframes.getfreesize())
				#print "HELLO"
			#else:
				#print "Page Fault"
				#print (freeframes.allocate())


			if(pid in pids):
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
				pids.append(pid)
			

		for i in pcb:
			print("Process " + str(i[0]) + " referenced " + str(i[1].getrefcount()) + " times.")
			print("Process " + str(i[0]) + " size: " + str(i[1].getpagecount()) + " pages.")
			

if __name__ == '__main__':
	main(sys.argv[1:])
