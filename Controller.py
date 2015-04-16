"""
Brendan Koning
4/16/2015
View.py
This file brings the model and view together by updating
the models and giving information to the view so that
it can update itself.
"""

import sys, getopt
from Model import stats, process, mainmemory
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
		self.currentprocess = None

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

	#Returns the process with the PID
	def getprocess(self, pid):
		return self.pcb[[x[0] for x in self.pcb].index(pid)][1]

	#Checks if the requested page is in memory, and faults if it is not
	def inmemory(self, pid, page):
		process = self.getprocess(pid)
		process.incref()
		#Page Already in Memory
		if(self.memory.isinmemory(pid, page)):
				index = self.memory.getindex(pid, page)
				print("Process " + str(pid) + " accessed Page " + str(page) + " on Frame " + str(index))
				return (index + 1) * -1
		#Page not in memory
		else:
			#Used to count faults for each process
			process.incfault()
			try:	
				#Indicates page was not in memory
				self.error = mainmemory.MemError
				index = self.memory.addtomemory(pid, page)
				print("Adding Process " + str(pid) + " Page " + str(page) + " to Frame " + str(index))
			except mainmemory.MemError:
				#Page is not in memory but memory is full
				self.error = mainmemory.MemError
				index = self.memory.lru(pid, page)
				print("Page Fault: Replacing Frame " + str(index) + " with Process " + str(pid) + " Page " + str(page))
			process.add(page, index)
			return index + 1

	#Actions to perform when pressing the "Next" button
	def nextstep(self):
		if(self.error != RuntimeError):
			line = self.file.readline()
			try:
				pid = line.split(":")[0][1]
			except IndexError:
				#This is when the program has ran to completion
				self.error = RuntimeError
				self.printinfo()
				self.view.pagetable()
				raw_input("Press Enter to Close")				
				exit()
			
			page = int(line.split(":")[1].strip(), 2)
			self.pcbmake(pid)
			index = self.inmemory(pid, page)
			self.memory.topofstack(pid, page)
			self.currentprocess = self.getprocess(pid)
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

if __name__ == '__main__':
	main(sys.argv[1:])
