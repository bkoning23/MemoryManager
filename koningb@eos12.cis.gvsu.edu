__author__ = 'Brendan Koning'

import sys
from Tkinter import *
from operator import itemgetter

class view(Frame):


	def loadView(self):
	    Label(self.frame, text="Physical Memory", bg="lightgray").grid(row=0, column=4)
	    for j in range(16):
	    	Label(self.frame, text=("Frame " + str(j)), bg="lightgray").grid(row=j+1, column=2)
	    	Label(self.frame, text="MemInfo", bg="lightgray").grid(row=j+1, column=4)
	   	
	   	Button(self.frame, text=("Next"), bg="lightgray", command=self.next).grid(row=20, column=2)
	   	Button(self.frame, text=("Next Fault"), bg="lightgray", command=self.nextfault).grid(row=20, column=3)
	   	Button(self.frame, text=("Run to Completion"), bg="lightgray", command=self.runtoend).grid(row=20, column=4)

	def __init__(self,vc):
		self.frame=Frame(bg="lightgray")
		self.frame.grid(row=0,column=0)
		self.vc = vc
		self.loadView()

	def pagetable(self):
		try:
			self.newWindow.destroy()
		except AttributeError:
			pass
		self.newWindow = Toplevel()
		pagetable = sorted(self.vc.currentprocess.getpages(), key=lambda process: process[0])

		Label(self.newWindow, text="Page Number", bg="lightgray").grid(row=0, column=2)
		Label(self.newWindow, text="Physical Frame", bg="lightgray").grid(row=0, column=4)
		for j in range(self.vc.currentprocess.getpagecount()):
			Label(self.newWindow, text=pagetable[j][0]).grid(row=j+1, column=2)
			Label(self.newWindow, text=pagetable[j][1]).grid(row=j+1, column=4)
		self.newWindow.title("P" + str(self.vc.currentprocess.getpid()) + " Page Table")
		self.newWindow.geometry("+400+100")


	def next(self):
		self.vc.nextstep()
		self.pagetable()

	def nextfault(self):
		self.vc.nextfault()
		self.pagetable()

	def runtoend(self):
		self.vc.runtocomplete()
		self.pagetable()
		
		
		

	
		




		
	

