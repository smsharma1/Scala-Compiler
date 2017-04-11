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
		self.objects = {}
		self.name = name
		self.parent = parent
		self.uid = SymbolTable.uid
		self.argList = argList
		self.returnType = returnType
		self.offset=0
		self.offsetmap={}
		self.itemcount=0
		self.size=0 #relevant for classes and objects
		SymbolTable.uid = SymbolTable.uid+1
		# print self.argList

	def LookUpVar(self, symbolName):
		scope = self
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.variables):
				pass
			else:
				return False
		while(scope):
			if symbolName in scope.variables:
				# print "hola ", scope.variables[symbolName]
				return scope.variables[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def LookUpFunc(self, symbolName, argList):
		scope = self
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.functions):
				pass
			else:
				return False
		while(scope):
		#	print "scope.functions " , scope.functions
			if symbolName in scope.functions:
			#	print scope.functions
				for func in scope.functions[symbolName]:
				#	print func.argList
					if argList == func.argList:
						return True
			scope = scope.parent
		return False
	
	def LookUpCurrentScope(self, symbolName):
		scope = self
		# print symbolName
		if symbolName in scope.variables:
			# print "inupsymbol",scope.variables[symbolName][1]
			return [self.variables[symbolName][1]]
		elif symbolName in scope.functions:
			# print self.functions[symbolName][0].returnType, " return type look up current scope"
			return [self.functions[symbolName][0].returnType]
		elif symbolName in scope.classes:
			return ['class', self.classes[symbolName][0].name]
		elif symbolName in scope.objects:
			# print self.objects[symbolName]
			return ['object', self.objects[symbolName][0].name]
		else:
			return False

# supposed to look for existential symbols
	def LookUpSymbolAcrossScope(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
				# print "inupsymbol",scope.variables[symbolName][1]
				return [self.variables[symbolName][1]]
			elif symbolName in scope.objects:
				# print self.objects[symbolName]
				return ['object', self.objects[symbolName][0].name]
			scope = scope.parent

	def LookUpSymbol(self, symbolName):
		scope = self
		while(scope):
			if symbolName in scope.variables:
			#	print "inupsymbol",scope.variables[symbolName][1]
				return scope.variables[symbolName][1]
			elif symbolName in scope.functions:
			#	print symbolName, " *******", (scope.functions[symbolName])[0].returnType  
				return (scope.functions[symbolName])[0].returnType
			scope = scope.parent
		return False

	def LookUpClass(self, symbolName, argList):
		# print symbolName, " ", argList
		# print self.name, " ", self.classes
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.objects):
				pass
			else:
				return False
		scope = self
		while(scope):
			# print scope.classes
			if symbolName in scope.classes:
				for class_name in scope.classes[symbolName]:
					# print class_name.argList
					if argList == class_name.argList:
						# print "i am i class"
						return True
			scope = scope.parent
		return False

	def LookUpObject(self, symbolName):
		scope = self
		# print symbolName, "symbolname in LookupObject"
		if(self.LookUpCurrentScope(symbolName)):
			if(symbolName in scope.objects):
				pass
			else:
				return False
		# print "am i here"
		while(scope):
			# print scope.objects
			if symbolName in scope.objects:
				# print  scope.objects[symbolName][0], " In Look up object"
				# print scope.objects[symbolName][0].name, " ", scope.objects[symbolName][0].variables, " "
				return scope.objects[symbolName]
			scope = scope.parent
#		print symbolName, " Variable not found"
		return False

	def GetFuncScope(self, symbolName, argList):
		scope = self
		while(scope):
		#	print "scope.functions " , scope.functions
			if symbolName in scope.functions:
				for func in scope.functions[symbolName]:
				#	print func.argList
					#print argList, " ", func.argList, "arglists in getfuncscope"
					if argList == func.argList:
						return func
			scope = scope.parent
		return False
	
	def GetClassScope(self, symbolName, argList):
		if symbolName in self.classes:
			for class_name in self.classes[symbolName]:
				if argList == class_name.argList:
					return class_name
			return False
		else:
			return False

	def LookDotThing(self,rootScope,symbolName):
		looklist = symbolName.split('.')
		name = ""
		myobject = self.LookUpObject(looklist[0])[0]
		# print myobject," myobject ",looklist[0]
		if myobject :
			if looklist[1] in myobject.functions:
				return [myobject.functions[looklist[1]][0].returnType]
			elif looklist[1] in myobject.variables:
				return [myobject.variables[looklist[1]][1]]		
		else:
			for name in looklist[:-1]:
				# print name," inelse ",rootScope.classes
				if name in rootScope.classes:
					rootScope = rootScope.classes[name]
				else:
					return False
			if name in rootScope.functions:
				for func in rootScope.functions[symbolName]:
					return [func.returnType]
			else:
				return False
		return False
	
	def GetOffset(self, symbolName):
		scope = self
		value = scope.LookUpSymbolAcrossScope(symbolName)
		if value == None:
			raise ValueError('An undeclared object: '+str(symbolName)+' is called for GetOffset')
		if value[0] == 'object':
			while(scope):
				if symbolName in scope.objects:
					raise ValueError("yet to fill code for finding offset of object")
			raise ValueError("unexpected behavior in GetOffset in object")
		while(scope):
			while(scope):
				if symbolName in scope.variables:
					return [self.variables[symbolName][3]]
			raise ValueError("unexpected behavior in GetOffset in variables")

	def LookUpArray(self, symbolName):
		scope=self
		if self.LookUpVar(symbolName):
			while(scope):
				if symbolName in self.variables:
					if self.variables[symbolName][2] > 0:
						return self.variables[symbolName]
					else:
						raise ValueError(symbolName+" is a variable and not an array")
		else:
			raise ValueError("No variable or array of this name found : "+symbolName)

	def LookUpSymbolType(self, symbolName):
		scope = self
		# print "ddddddd",symbolName
		while(scope):
			value = scope.LookUpCurrentScope(symbolName)
			if(value):
				# print value
				return value
			scope = scope.parent
		return False

	def SetObjectName(self, currentName, newName):
		# print "Insetobjectname", currentName," ",newName
		myobject = self.LookUpObject(currentName)
		# print myobject, "myobject"
		self.objects[newName] = copy.deepcopy(myobject)
		self.objects.pop(currentName, None)
		# commenting out following line because space for object pointer already 
		# alloted at the time of creation of temp object
		# self.offset = self.offset + self.objects[newName].getSymbolTableSize()
		# print self.objects[newName][0], "last line in set object name"

	def InsertVar(self, symbolName, val, type_name, length=0):
		# print "testing",type_name
		global esp
		if self.LookUpCurrentScope(symbolName):
			raise ValueError("InsertVar called on "+symbolName+" but it is already declared")
		else:
			self.variables[symbolName] = [val, type_name, length, self.offset]
			if length:
				self.offset = self.offset + self.Size(type_name.upper())*length
				esp = esp + self.Size(type_name.upper())*length
				self.offsetmap[offset] = self.itemcount
				activr.push(val)
				self.itemcount = self.itemcount + 1
			else:
				self.offset = self.offset + self.Size(type_name.upper())
				esp = esp + self.Size(type_name.upper())
				self.offsetmap[offset] = self.itemcount
				activr.push(val)
				self.itemcount = self.itemcount + 1

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
		# print symbolName, " ", className, " insert object***************"
		if self.LookUpCurrentScope(symbolName):
			raise ValueError(symbolName+" is already declared")
		scope = self
		while(scope):
			if className in scope.classes:
				# print  "className"
				class_name = scope.classes[className][0]
				self.objects[symbolName] = [copy.deepcopy(class_name), className, self.offset] #notice that we actually need self here instead of scope
				self.offset = self.offset + self.Size("POINTER")
				esp = esp + self.Size("POINTER")
				self.offsetmap[offset] = self.itemcount
				activr.push("POINTER")
				self.itemcount = self.itemcount + 1
				# print class_name, " ", self.objects[symbolName],"after deepcopy"
				# self.InvokeConstr(self.objects[symbolName], valList)
				return True
			scope = scope.parent
			
		# print "%s not found" % (className)
		return False

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
	#	print symbolName, " ", argList, " ", returnType
	#	print "hello in insertfuncdetails"
		self.argList = argList
		self.name = symbolName
		self.returnType = returnType

	def InvokeConstr(self, classScope, valList):
		# you can get arglist from scope.arglist to parse valList
		pass

	def Dumper(self, scope, fileh):
		# column description
		# return Type
		# type name ActType/class type
		# print scope.name , fileh
		buffer = ""
		# print scope.variables, "i am symbol table"
		# print scope.objects, "i am symbol table"
		# print scope.name, " in dumper"
		offset = 0
		fileh.write(scope.name+"\n")
		for key in scope.variables:
			if(scope.variables[key][1]=="STRING"):
				size = scope.variables[key][2]*2
				prevoffset = offset
				offset = offset + size
			elif(scope.variables[key][1][5:10]=="ARRAY"):
				typename = self.Size(scope.variables[key][1][10:])
				# print typename, scope.variables[key][2]
				size = int(scope.variables[key][2])*typename
				prevoffset = offset
				offset = offset + size
			elif(scope.variables[key][1][0:5]=="ARRAY"):
				typename = self.Size(scope.variables[key][1][5:])
				# print typename, scope.variables[key][2]
				size = int(scope.variables[key][2])*typename
				prevoffset = offset
				offset = offset + size
			else:
				size = self.Size(scope.variables[key][1])
				prevoffset = offset
				offset = offset + size
			buffer = "var, " + str(key) +", "+ str(scope.variables[key][1])+ ", " + str(size) + ", " + str(prevoffset)+ "\n"
			fileh.write(buffer)
		for key in scope.objects:
			buffer = "object, " + str(key) + ", "+ str(scope.objects[key][0].name) +", \n"
			fileh.write(buffer)
		for key in scope.functions:
			arglist = str(scope.functions[key][0].argList)
			buffer = "function, " + str(key) + ", " + arglist+ "-->" + str(scope.functions[key][0].returnType)+",  " + " \n"
			fileh.write(buffer)
		fileh.write('\n')

	def Size(self, type1 ):
		if type1=="INT":
			return 4
		elif type1=="CHAR":
			return 2
		elif type1=="BYTE":
			return 1
		elif type1=="SHORT":
			return 2
		elif type1=="LONG":
			return 8
		elif type1=="FLOAT":
			return 4
		elif type1=="DOUBLE":
			return 8
		elif type1=="POINTER":
			return 4
		elif "ARRAY" in type1:
			return self.Size(type1.replace("ARRAY", ''))
		else:
			return 10