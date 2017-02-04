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
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   parser.parse(s)
   graph.write_png('parsetree.png')
