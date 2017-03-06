class Dictlist(dict):
	def __setitem__(self, key, value):
		try:
			self[key]
		except KeyError:
			super(Dictlist, self).__setitem__(key, [])
		self[key].append(value)

class SymbolTable:
	uid = 0
	def __init__(self, parent, name, argList=[], returnType=None): # parent scope and symbol table name
		self.functions = Dictlist()
		self.variables = {}
		self.name = name
		self.parent = parent
		self.uid = SymbolTable.uid
		self.argList = argList
		self.returnType = returnType
		SymbolTable.uid = SymbolTable.uid+1
		print self.argList

	def LookUpVar(self, symbolName):
		if symbolName in self.variables:
			return self.variables[symbolName]

	def LookUpFunc(self, symbolName, argList):
		print symbolName, " ", argList
		print self.name, " ", self.functions
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				print func.argList
				if argList == func.argList:
					return True
			return False
		else:
			return False

	def GetScope(self, symbolName, argList):
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList:
					return func
			return False
		else:
			return False

	def InsertVar(self, symbolName, val):
		if symbolName in self.variables:
			return 0
		else:
			self.variables[symbolName] = val

	def InsertFunc(self, symbolName, argList, returnType):
		print symbolName, " ", argList, " ", returnType
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList and self.returnType == returnType:
					return False
			self.functions[symbolName] = SymbolTable(self.name, symbolName, argList=argList, returnType=returnType)
		else:
			self.functions[symbolName] = SymbolTable(self.name, symbolName, argList=argList, returnType=returnType)
			print self.functions
			
