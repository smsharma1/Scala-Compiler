class Dictlist(dict):
	def __setitem__(self, key, value):
		try:
			self[key]
		except KeyError:
			super(Dictlist, self).__setitem__(key, [])
		self[key].append(value)

class SymbolTable(object):
	uid = 0
	def __init__(self, parent, name, argList=[]): # parent scope and symbol table name
		self.functions = Dictlist()
		self.variables = {}
		self.name = name
		self.parent = parent
		self.uid = SymbolTable.uid
		self.argList = argList
		SymbolTable.uid = SymbolTable.uid+1

	def LookUpVar(self, symbolName):
		if symbolName in self.variables:
			return self.variables[symbolName]

	def LookUpFunc(self, symbolName, argList):
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList:
					return True
			return False
		else:
			return False

	def InsertVar(self, symbolName, val):
		if symbolName in self.variables:
			return 0
		else:
			self.variables[symbolName] = val

	def InsertFunc(self, symbolName, argList):
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList:
					return False
			self.functions[symbolName] = SymbolTable(self.name, symbolName, argList=argList)
		else:
			self.functions[symbolName] = SymbolTable(self.name, symbolName, argList=argList)
			
