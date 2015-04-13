__author__ = 'Brendan'

import sys
from Tkinter import *

class view(Frame):


	def loadView(self):
	    Label(self.frame, text="Physical Memory", bg="lightgray").grid(row=0, column=4)
	    for j in range(16):
	    	Label(self.frame, text=("Frame " + str(j)), bg="lightgray").grid(row=j+1, column=2)
	    	Label(self.frame, text="MemInfo", bg="lightgray").grid(row=j+1, column=4)
	   	
	   	Button(self.frame, text=("Next"), bg="lightgray", command=self.pagetable).grid(row=20, column=2)
	   	Button(self.frame, text=("Next Fault"), bg="lightgray", command=self.vc.nextfault).grid(row=20, column=3)
	   	Button(self.frame, text=("Run to Completion"), bg="lightgray", command=self.vc.runtocomplete).grid(row=20, column=4)

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
		for j in range(16):
			Label(self.newWindow, text="MemInfo", bg="lightgray").grid()
		self.newWindow.title("Page Table")
		self.newWindow.geometry("+400+100")
		Label(self.newWindow, text="Physical Memory", bg="lightgray").grid(row=0, column=4)
		self.vc.nextstep()

	
		




		
	

