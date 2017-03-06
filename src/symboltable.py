import copy

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
		self.classes = Dictlist()
		self.objects = Dictlist()
		self.name = name
		self.parent = parent
		self.uid = SymbolTable.uid
		self.argList = argList
		self.returnType = returnType
		SymbolTable.uid = SymbolTable.uid+1
		# print self.argList

	def LookUpVar(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
				return scope.variables[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def LookUpFunc(self, symbolName, argList):
		scope = self
		while(scope):
			print "scope.functions " , scope.functions
			if symbolName in scope.functions:
				for func in scope.functions[symbolName]:
				#	print func.argList
					if argList == func.argList:
						return True
			scope = scope.parent
		return False
	
	def LookUpSymbol(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
				return scope.variables[symbolName][1]
			elif symbolName in scope.functions:
				print symbolName, " *****************************************"
				return (scope.functions[symbolName])[0].returnType
			scope = scope.parent
		return False

	def LookUpClass(self, symbolName, argList):
		# print symbolName, " ", argList
		# print self.name, " ", self.classes
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				# print class_name.argList
				if argList == class_name.argList:
					return True
			return False
		else:
			return False

	def LookUpObject(self, symbolName):
		if symbolName in self.variables:
			return self.variables[symbolName]
		else:
		#print "Object not found"
			return False

	def GetFuncScope(self, symbolName, argList):
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList:
					return func
			return False
		else:
			return False
	
	def GetClassScope(self, symbolName, argList):
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return class_name
			return False
		else:
			return False

	def InsertVar(self, symbolName, val, type_name):
		if symbolName in self.variables:
			return False
		else:
			self.variables[symbolName] = [val, type_name]

	def InsertFunc(self, symbolName, argList, returnType):
#		print symbolName, " ", argList, " ", returnType
		if symbolName in self.functions:
			for func in self.functions[symbolName]:
				if argList == func.argList and self.returnType == returnType:
					return False
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
		else:
			self.functions[symbolName] = SymbolTable(self, symbolName, argList=argList, returnType=returnType)
			# print self.functions
		return self.functions[symbolName][0]
	
	def InsertClass(self, symbolName, argList):
		# print symbolName, " " , argList
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return False
			self.classes[symbolName] = SymbolTable(self, symbolName, argList=argList)
		else:
			self.classes[symbolName] = SymbolTable(self, symbolName, argList=argList)
			# print self.classes
		return self.classes[symbolName][0]
	
	def InsertObject(self, symbolName, className, valList):
		# print symbolName, " "
		if className in self.classes:
			class_name = self.classes[className]
			self.objects[symbolName] = copy.deepcopy(class_name)
			self.InvokeConstr(self.objects[symbolName], valList)
		else:
			print "%s not found" % (className)

	def InsertSingletonObject(self, symbolName):
		self.singletonObject = SymbolTable(self, symbolName)
		return self.singletonObject

	# def setName(self, symbolName):
	# 	self.name = symbolName

	# def setArglist(self, argList):
	# 	self.argList = argList

	# def setReturnType(self, returnType):
	# 	self.returnType = returnType

	def NewFuncScope(self):
		return SymbolTable(self, "temp")

	def InsertFuncDetails(self, symbolName, argList, returnType):
#print symbolName, " ", argList, " ", returnType
		self.argList = argList
		self.name = symbolName
		self.returnType = returnType

	def InvokeConstr(self, classScope, valList):
		# you can get arglist from scope.arglist to parse valList
		pass