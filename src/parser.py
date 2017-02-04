# Yacc example

import ply.yacc as yacc
import pydot

# Get the token map from the lexer.  This is required.
from lexer import tokens
graph = pydot.Dot(graph_type='digraph')

class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
	 par = pydot.Node(type, style="filled", fillcolor="red")
	 graph.add_node(par)
         if children:
              self.children = children
	      for ch in children:
	          graph.add_edge(pydot.Edge(par, ch))	
         else:
              self.children = [ ]
         self.leaf = leaf
         for l in leaf:
	      n = pydot.Node(l, style="filled", fillcolor="red")
	      graph.add_edge(pydot.Edge(par, n))

def p_literals(p):
    '''literals : INT 
		| FLOAT 
		| STRING 
		| CHAR'''
    Node("literals",None,[p[1]])

# Build the parser


def p_QualId(p):
	'''QualId : ID 
	| ID DOT QualId'''
	if(len(p) == 2):
		p[0] = Node("QualId", None, [p[1]] )
	else:
		p[0] = Node("QualId", [p[3]], [p[1],p[2]])

def p_Ids(p):
	'''Ids : ID 
	| ID COMMA Ids'''
	if(len(p) == 2):
		p[0] = Node("Ids", None, [p[1]] )
	else:
		p[0] = Node("Ids", [p[3]], [p[1],p[2]])

def p_Path(p):
	'''Path : StableId 
	| ID DOT R_THIS 
	| R_THIS'''
	if(len(p) == 2):
		if(p[1] == "this"):
			p[0] = Node("Path", None, [p[1]] )
		else:
			p[0] = Node("Path", [p[1]],None )
	else:
		p[0] = Node("Path",None,  [p[1],p[2],p[3]])

def p_StableId(p):
	'''StableId :  ID 
	| Path DOT ID 
	| R_SUPER DOT ID 
	| ID DOT R_SUPER DOT ID '''
	# | ID DOT R_SUPER ClassQualifier DOT ID 
	# | R_SUPER ClassQualifier DOT ID'''
	if(len(p) == 2):
		p[0] = Node("StableId", None, p[1] )
	elif(len(p)==4):
		if(p[2] == "super"):
			p[0] = Node("StableId",None, [p[1], p[2], p[3]])
		else:
			p[0] = Node("StableId", [p[1]], [p[2],p[3]])
	elif(len(p)==5):
		p[0] = Node("StableId", [p[2]], [p[1],p[3], p[4]])
	elif(len(p)==6):
		p[0] = Node("StableId", None, [p[1], p[2], p[3], p[4], p[5]])
	else:
		p[0] = Node("StableId", [p[4]], [p[1], p[2], p[3], p[5], p[6]])


# def p_QualId(p):
# 	'''expression : ID | DOT expression'''
# 	if(len(p) == 2):
# 		p[0] = Node("QualId", None, p[1] )
# 	else:
# 		p[0] = Node("QualId", [p[1],[3]], p[2])


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

parser = yacc.yacc()

while True:
   try:
	   s = raw_input('calc > ')
   except EOFError:
	   break
   if not s: continue
   parser.parse(s)
   graph.write_png('parsetree.png')
