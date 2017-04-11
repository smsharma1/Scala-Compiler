class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

	def access(self, num):
		return self.items[num]

	def relAccess(self, num, ebp):
		return self.items[num+ebp]
	
	def relModify(self, num, ebp):
		return self.items[num+ebp]
