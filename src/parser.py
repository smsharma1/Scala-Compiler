# Yacc example

import ply.yacc as yacc
import pydot
# import graphviz as gv
# Get the token map from the lexer.  This is required.
from lexer import tokens
graph = pydot.Dot(graph_type='digraph')

class Node:
	uid=0
	def __init__(self,type,children,leaf,isChild=False):
		self.type = type
		Node.uid = Node.uid + 1
		self.uid = Node.uid
		self.name = type+" "+str(self.uid)
		if isChild:
			self.node = pydot.Node(self.name, style="filled", fillcolor="green")
		else:
			self.node = pydot.Node(self.name, style="filled", fillcolor="red")
		graph.add_node(self.node)
		print children, " children"
		self.children = children
		for l in leaf:
			term = Node(l, [], [],True).name
			graph.add_edge(pydot.Edge(self.name, term))
		for ch in self.children:
			graph.add_edge(pydot.Edge(self.name, ch))
		self.leaf = leaf
		print leaf, " leaf"


def p_QualId(p):
	'''QualId : ID 
		| ID DOT QualId'''
	print(p[0])
	if(len(p) == 2):
		p[0] = Node("QualId " , [], [p[1]] ).name
		print "in if"
	else:
		print p[3]
		p[0] = Node("QualId", [p[3]], [p[1],p[2]]).name
		print "in else"


def p_literals(p):
	'''literals : INT 
		| FLOAT 
		| STRING 
		| CHAR'''
	print("sharma")
	p[0] = Node("literals",None,[p[1]])
	return "literals"

# def p_CompilationUnit(p):
# 	'''CompilationUnit : TopStatSeq 
# 	|	R_PACKAGE QualId semi CompilationUnit ''' 
# 	if len(p) == 2:
# 		p[0] = Node(CompilationUnit,[p[1]],None)
# 	else:
# 		p[0] = Node(CompilationUnit,[p[2],p[3],p[4]],[p[1]])


# Build the parser

def p_Ids(p):
		"Ids : ID "
		if(len(p) == 2):
				p[0] = Node("Ids", [], [p[1]] )
		else:
				p[0] = Node("Ids", [p[3]], [p[1],p[2]])



# def p_Ids(p):
# 	'''Ids : ID 
# 	| ID COMMA Ids'''
# 	if(len(p) == 2):
# 		p[0] = Node("Ids", None, [p[1]] )
# 	else:
# 		p[0] = Node("Ids", [p[3]], [p[1],p[2]])

# def p_QualId(p):
# 	'''QualId : ID 
# 	| ID DOT QualId'''
# 	if(len(p) == 2):
# 		p[0] = Node("QualId", None, [p[1]] )
# 	else:
# 		p[0] = Node("QualId", [p[3]], [p[1],p[2]])	


# def p_Path(p):
# 	'''Path : StableId 
# 	| ID DOT R_THIS 
# 	| R_THIS'''
# 	if(len(p) == 2):
# 		if(p[1] == "this"):
# 			p[0] = Node("Path", None, [p[1]] )
# 		else:
# 			p[0] = Node("Path", [p[1]],None )
# 	else:
# 		p[0] = Node("Path",None,  [p[1],p[2],p[3]])

# def p_StableId(p):
# 	'''StableId :  ID 
# 	| Path DOT ID 
# 	| R_SUPER DOT ID 
# 	| ID DOT R_SUPER DOT ID '''
# 	# | ID DOT R_SUPER ClassQualifier DOT ID 
# 	# | R_SUPER ClassQualifier DOT ID'''
# 	if(len(p) == 2):
# 		p[0] = Node("StableId", None, p[1] )
# 	elif(len(p)==4):
# 		if(p[2] == "super"):
# 			p[0] = Node("StableId",None, [p[1], p[2], p[3]])
# 		else:
# 			p[0] = Node("StableId", [p[1]], [p[2],p[3]])
# 	elif(len(p)==5):
# 		p[0] = Node("StableId", [p[2]], [p[1],p[3], p[4]])
# 	elif(len(p)==6):
# 		p[0] = Node("StableId", None, [p[1], p[2], p[3], p[4], p[5]])
# 	else:
# 		p[0] = Node("StableId", [p[4]], [p[1], p[2], p[3], p[5], p[6]])




# Error rule for syntax errors
# def p_error(p):
# 	print("Syntax error in input!")


parser = yacc.yacc()

while True:
	try:
		s = raw_input('calc > ')
	except EOFError:
		break
	if not s: continue
	parser.parse(s)
	graph.write_png('parsetree.png')
	graph.to_string()
	print(graph.to_string())
