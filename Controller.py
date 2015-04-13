__author__ = 'Brendan'

import sys, getopt
from Model import stats, process, freeframelist, mainmemory
from View import view
from Tkinter import *

class controller():
	def __init__(self, parent, argv):
		self.parent = parent
		self.view = view(self)
		self.file = open(argv[0], 'r')
		self.pids = []
		self.pcb = []
		self.memory = mainmemory(16)
		self.error = None
		self.replaceframe = Frame()
		self.accessframe = Frame()

	def pcbmake(self, pid):
		if(pid in self.pids):
			pass
		else:
			#This is if the process has not been recorded yet
			self.pcb.append((pid, process(pid)))
			self.pids.append(pid)

	def printinfo(self):
		for i in self.pcb:
			print("Process " + str(i[0]) + " referenced " + str(i[1].getrefcount()) + " times.")
			print("Process " + str(i[0]) + " size: " + str(i[1].getpagecount()) + " pages.")
			print("Process " + str(i[0]) + " faulted " + str(i[1].getfaultcount()) + " times.")
			#print(i[1].getpagetable())

	def inmemory(self, pid, page):
		process = self.pcb[[x[0] for x in self.pcb].index(pid)][1]
		process.incref()
		#Page Already in Memory
		if(self.memory.isinmemory(pid, page)):
				index = self.memory.getindex(pid, page)
				print("Process " + str(pid) + " accessed Page " + str(page) + " on Frame " + str(index))
				return (index + 1) * -1
		#Page not in memory
		else:
			process.incfault()
			try:	
				self.error = mainmemory.MemError
				index = self.memory.addtomemory(pid, page)
				print("Adding Process " + str(pid) + " Page " + str(page) + " to Frame " + str(index))
			except mainmemory.MemError:
				self.error = mainmemory.MemError
				index = self.memory.lru(pid, page)
				print("Page Fault: Replacing Frame " + str(index) + " with Process " + str(pid) + " Page " + str(page))
			process.add(page, index)
			return index + 1

	def nextstep(self):
		if(self.error != RuntimeError):
			line = self.file.readline()
			try:
				pid = line.split(":")[0][1]
			except IndexError:
				self.error = RuntimeError
				self.printinfo()
				raw_input("Press Enter to Close")				
				exit()

			page = int(line.split(":")[1].strip(), 2)
			self.pcbmake(pid)
			index = self.inmemory(pid, page)
			self.memory.topofstack(pid, page)
			#This is so only one frame will ever be colored at a time
			#which represents the last action done.
			#Red = Page Fault
			#Green = Page Access
			self.replaceframe.config(bg="lightgray")
			self.accessframe.config(bg="lightgray")
			#Page replacement
			if (index > 0):	
				self.replaceframe = (self.view.frame.grid_slaves(column=4, row=index))[0]
				self.replaceframe.config(text=("P" + str(pid) + "    Page " + str(page)), bg="red")
			#Page access
			else:
				index = index * -1
				self.accessframe = self.view.frame.grid_slaves(column=4,row=(index))[0]
				self.accessframe.config(bg="green")

	def nextfault(self):
		if(self.error != RuntimeError):
			while(self.error != mainmemory.MemError):
				self.nextstep()
			print("Went to next fault")
			self.error = None

	def runtocomplete(self):
		while(self.error != RuntimeError):
			self.nextstep()

	

	


def main(argv):
	root = Tk()
	frame = Frame(root, bg='lightgray')
	root.title('Memory Manager')
	app = controller(root, argv)
	root.mainloop()


'''
def main(argv):
	gui = view()
	gui.addbutton()
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
			#raw_input(" ")
			#Process ID
			pid = line.split(":")[0][1]
			#Requested Page
			page = int(line.split(":")[1].strip(), 2)
			print ("Process " + str(pid) + " accessed Page " + str(page))
			
			#Checks if there is already a PCB
			if(pid in pids):
				#This is the index of the tuple that contains the 
				#pcb corresponding to the pid
				#a = [x[0] for x in pcb].index(pid)
				#a is the index of the process in the PCB, 1
				#should be hardcoded because it is the second 
				#item in the tuple.
				#pcb[a][1].add(page)
				pass
			else:
				#This is if the process has not been recorded yet
				pcb.append((pid, process(pid)))
				pids.append(pid)

			a = [x[0] for x in pcb].index(pid)
			pcb[a][1].incref()

			#check if page is in memory
			if(memory.isinmemory(pid, page)):
				pass
				#print("ITS IM MEMEORY")
			else:
				#print ("NOT IN MEMORY")
				pcb[a][1].incfault()
				try:	
					index = memory.addtomemory(pid, page)
					print("adding " + str(pid) + " " + str(page) + " to index " + str(index))
				except mainmemory.MemError:
					print ("OUT OF MEMORY LRU REPLACE")
					index = memory.lru(pid, page)
					print("adding " + str(pid) + " " + str(page) + " to index " + str(index))
				pcb[a][1].add(page, index)

			memory.topofstack(pid, page)
			print(memory.getstack())
			print(memory.getmem())
			print(pcb[a][1].getpages())
			print(memory)
			print(pcb[a][1].getpagetable())



			#if(freeframes.isempty()):
				#print(freeframes.getfreesize())
				#print "HELLO"
			#else:
				#print "Page Fault"
				#print (freeframes.allocate())

		for i in pcb:
			print("Process " + str(i[0]) + " referenced " + str(i[1].getrefcount()) + " times.")
			print("Process " + str(i[0]) + " size: " + str(i[1].getpagecount()) + " pages.")
			print("Process " + str(i[0]) + " faulted " + str(i[1].getfaultcount()) + " times.")
			print(i[1].getpagetable())
'''			

if __name__ == '__main__':
	main(sys.argv[1:])
