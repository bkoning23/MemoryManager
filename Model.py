__author__ = 'Brendan'

from collections import deque

class stats:
	def __init__(self):
		self.proceses = []

	def add(self, id):
		self.proceses.append(id)

	def count(self):
		return len(set(self.proceses))

class process:
	def __init__(self, id):
		self.refcount = 0
		self.pagefault = 0
		self.pages = []
		self.pid = id

	def add(self, page, frame):
		for i in self.pages:
			if(i[0] == page):
				self.pages.remove(i)
		self.pages.append((page, frame))

	def getpages(self):
		return self.pages

	def getpagecount(self):
		return len(set(self.pages))

	def getrefcount(self):
		return self.refcount

	def getfaultcount(self):
		return self.pagefault

	def getall(self):
		return (self.pages, self.refcount, self.pid)

	def incref(self):
		self.refcount += 1

	def incfault(self):
		self.pagefault += 1

	def getpagetable(self):
		s = ("Process " + self.pid + ":\n")
		s += ("Page\tFrame\n")
		for x in range(len(self.pages)):
			s += (str(self.pages[x][0]) + "\t" + str(self.pages[x][1]) + "\n")
		return s

	def __str__(self):
		return str(self.refcount)

class freeframelist:
	def __init__(self, size):
		self.freeframes = range(size)

	def getfree(self):
		return self.freeframes

	def getfreesize(self):
		return len(self.freeframes)

	def isempty(self):
		if not self.freeframes:
			return True
		return False

	def allocate(self):
		return self.freeframes.pop()

class mainmemory:
	class MemError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

	def __init__(self, total):
		self.memory = []
		#In refstack, left is most recently used, right 
		#is what will be removed if needed
		self.refstack = deque([])
		self.size = total
		self.e = None

	def __str__(self):
		s = ("Frame #\t ProcID\t Page#\n")
		for x in range(len(self.memory)):
			curr = self.memory[x]
			pid = curr[0]
			page = curr[1]
			s += (str(x) + "\t" + str(pid) + "\t" + str(page) + "\n")
		return s

	def getmem(self):
		return self.memory

	def isinmemory(self, pid, page):
		return (pid, page) in self.memory

	def getindex(self, pid, page):
		try:
			return (self.memory.index((pid, page)))
		except ValueError, ex:
			self. e = ex

	#Puts the index of the (pid, page) tuple in memory as the 
	#most recently used.
	def topofstack(self, pid, page):
		index = self.getindex(pid, page)
		if not self.e:
			try:
				self.refstack.remove(index)
			except ValueError:
				pass
			self.refstack.appendleft(self.getindex(pid, page))

	def addtomemory(self, pid, page):
		if(len(self.memory) >= self.size):
			raise self.MemError("Out of Memory")
		self.memory.append((pid, page))
		return self.memory.index((pid, page))

	def getstack(self):
		return self.refstack

	#Determines the LRU page and replaces it	
	def lru(self, pid, page):
		#Index of main mem page to be replaced
		index = self.refstack.pop()
		#Removes the frame at the specified index and replaces it
		self.memory.pop(index)
		self.memory.insert(index, (pid, page))
		return index




	



