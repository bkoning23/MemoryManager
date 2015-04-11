__author__ = 'Brendan'

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
		self.pages = []
		self.pid = id

	def add(self, page):
		self.pages.append(page)
		self.refcount += 1

	def getpages(self):
		return self.pages

	def getrefcount(self):
		return self.refcount

	def __str__(self):
		return self.pages

