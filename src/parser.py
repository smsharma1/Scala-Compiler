# Yacc example

import ply.yacc as yacc
import pydot
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
		print leaf, " leaf"
		self.leaf = leaf
		for l in leaf:
			term = Node(l, [], [],True).name
			graph.add_edge(pydot.Edge(self.name, term))
		for ch in self.children:
			graph.add_edge(pydot.Edge(self.name, ch))

def p_QualId(p):
	'''QualId : ID 
		| ID DOT QualId'''
	print "p[0] : ",p[0]
	if(len(p) == 2):
		p[0] = Node("QualId" , [], [p[1]] ).name
		print "in if"
	else:
		print p[3]
		p[0] = Node("QualId", [p[3]], [p[2], p[1]]).name
		print "in else"

def p_CompilationUnit(p):
	'''CompilationUnit : TopStatSeq 
	|	R_PACKAGE QualId semi CompilationUnit ''' 
	if len(p)==2:
		p[0] = Node("CompilationUnit", [p[1]],[]).name
	else:
		p[0] = Node("CompilationUnit", [p[2],p[3],p[4]],[p[1]]).name

def p_PackageObject(p):
	'PackageObject : R_PACKAGE R_OBJECT ObjectDef'
	p[0] = Node("PackageObject", [p[3]],[p[2],p[1]]).name

def p_Packaging(p):
	'''Packaging : R_PACKAGE QualId 
	| R_PACKAGE QualId n1 
	| Packaging TopStatSeq '''
	if len(p)==4:
		p[0] = Node("Packaging", [p[2],p[3]],[p[1]]).name
	elif p[1] == "package":
		p[0] = Node("Packaging", [p[2]], [p[1]]).name
	else:
		p[0] = Node("Packaging", [p[1],p[2]],[]).name

def p_TopStat(p):
	'''TopStat : Import 
				| Packaging
				| PackageObject
			    | TopStat1 TopStat2 TmplDef
				| empty '''
	if len(p)==4:
		p[0] = Node("TopStat", [p[2],p[3],p[4]],[]).name
	elif "Import" in p[1]:
		p[0] = Node("TopStat", [p[1]], []).name
	elif "Packaging" in p[1]:
		p[0] = Node("TopStat", [p[1]], []).name
	elif "PackageObject" in p[1]:
		p[0] = Node("TopStat", [p[1]],[]).name
	else:
		p[0] = Node("TopStat", [p[1]],[]).name
	
def p_TopStat1(p):
	'''TopStat1 : empty
				| Annotation 
				| Annotation nl
				| TopStat1 Annotation 
				| TopStat1 Annotation nl'''
	if len(p)==4:
		p[0] = Node("TopStat1", [p[1],p[2],p[3]],[]).name
	elif "TopStat1" in p[1]:
		p[0] = Node("TopStat1", [p[1], p[2]], []).name
	elif "nl" in p[2]:
		p[0] = Node("TopStat1", [p[1], p[2]], []).name
	elif "Annotation" in p[1]:
		p[0] = Node("TopStat1", [p[1]],[]).name
	else :
		p[0] = Node("TopStat1", [p[1]],[]).name

def p_Modifier0more(p):
	'''Modifier0more : empty 
				| Modifier0more Modifier'''
	if len(p)==3:
		p[0] = Node("Modifier0more", [p[2],p[3]],[]).name
	elif "Import" in p[1]:
		p[0] = Node("Modifier0more", [p[1]], []).name
	else:
		p[0] = Node("Modifier0more", [p[1]],[]).name

#look for semi
def p_TopStatSeq(p):
	'''TopStatSeq : semi TopStat 
				  | TopStat TopStatSeq'''
	if "TopStat" in p[1]:
		p[0] = Node("TopStatSeq", [p[1],p[2]],[]).name
	else:
		p[0] = Node("TopStatSeq", [p[1],p[2]],[]).name

def p_SelfInvocation(p):
	'''SelfInvocation : R_THIS ArgumentExprs
					  | SelfInvocation ArgumentExprs'''
	if "this" in p[1]:
		p[0] = Node("SelfInvocation", [p[2]],[p[1]]).name
	else:
		p[0] = Node("SelfInvocation", [p[1],p[2]],[]).name

def p_ConstrBlock(p):
	'ConstrBlock : BLOCKOPEN SelfInvocation ConstrBlock1 BLOCKCLOSE '
	p[0] = Node("ConstrBlock", [p[2],p[3]],[p[1],p[4]]).name

def p_ConstrBlock1(p):
	'''ConstrBlock1 : empty 
					| semi BlockStat'''
	if "semi" in p[1]:
		p[0] = Node("ConstrBlock1", [p[1],p[2]], []).name
	else:
		p[0] = Node("ConstrBlock1", [p[1],p[2]],[]).name

def p_ConstrExpr(p):
	'''ConstrExpr : SelfInvocation 
				  | ConstrBlock'''
	if "ConstrBlock" in p[1]:
		p[0] = Node("ConstrExpr", [p[1]], []).name
	else:
		p[0] = Node("ConstrExpr", [p[1]],[]).name

def p_EarlyDef(p):
	'EarlyDef : TopStat1 TopStat2 PatVarDef'
	p[0] = Node("EarlyDef", [p[1], p[2], p[3]],[]).name

def p_EarlyDefs(p):
	'EarlyDefs : BLOCKOPEN EarlyDefs1 BLOCKCLOSE R_WITH'
	p[0] = Node("EarlyDefs", [p[2]], [p[1], p[3], p[4]]).name

def p_EarlyDefs1(p):
	'''EarlyDefs1 : empty 
				  | EarlyDef EarlyDefs2'''
	if "EarlyDef" in p[1]:
		p[0] = Node("EarlyDefs1", [p[1], p[2]], []).name
	else:
		p[0] = Node("EarlyDefs1", [p[1]],[]).name
		
def p_EarlyDefs2(p):
	'''EarlyDefs2 : empty 
				  | semi EarlyDef EarlyDefs2'''
	if "semi" in p[1]:
		p[0] = Node("EarlyDefs2", [p[1], p[2], p[3]], []).name
	else:
		p[0] = Node("EarlyDefs2", [p[1]],[]).name

def p_Constr(p):
	'''Constr : AnnotType 
			  | AnnotType ArgumentExprs0more'''
	if len(p)==3:
		p[0] = Node("Constr", [p[1], p[2]], []).name
	else:
		p[0] = Node("Constr", [p[1]],[]).name
	
def p_ArgumentExprs0more(p):
	'''ArgumentExprs0more : empty 
					   | ArgumentExprs0more ArgumentExprs'''
	if len(p)==3:
		p[0] = Node("ArgumentExprs0more", [p[1], p[2]], []).name
	else:
		p[0] = Node("ArgumentExprs0more", [p[1]],[]).name
	
def p_TraitParents(p):
	'''TraitParents : AnnotType 
					| WithAnnotType0more'''
	if "WithAnnotType0more" in p[1]:
		p[0] = Node("TraitParents", [p[1]], []).name
	else:
		p[0] = Node("TraitParents", [p[1]],[]).name

def p_WithAnnotType0more(p):
	'''WithAnnotType0more : empty
							| WithAnnotType0more R_WITH AnnotType'''
	if "WithAnnotType0more" in p[1]:
		p[0] = Node("WithAnnotType0more", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("WithAnnotType0more", [p[1]],[]).name

def p_ClassParents(p):
	'ClassParents : Constr WithAnnotType0more'
	p[0] = Node("ClassParents", [p[1], p[2]], []).name

def p_TraitTemplate(p):
	'TraitTemplate : EarlyDefs01 TraitParents TemplateBody01'
	p[0] = Node("TraitTemplate", [p[1], p[2], p[3]], []).name

def p_EarlyDefs01(p):
	'''EarlyDefs01 : empty 
					| EarlyDefs'''
	p[0] = Node("EarlyDefs01", [p[1]], []).name

def p_TemplateBody01(p):
	'''TemplateBody01 : empty 
						| TemplateBody'''
	p[0] = Node("TemplateBody01", [p[1]], []).name

def p_ClassTemplate(p):
	'ClassTemplate : EarlyDefs01 ClassParents TemplateBody01'
	p[0] = Node("ClassTemplate", [p[1], p[2], p[3]], []).name

def p_TraitTemplateOpt(p):
	'''TraitTemplateOpt : R_EXTENDS TraitTemplate
					 | Extends01TemplateBody01'''
	if len(p)==2
		p[0] = Node("TraitTemplateOpt", [p[2]], [p[1]]).name
	else:
		p[0] = Node("TraitTemplateOpt", [p[1]],[]).name

def  p_Extends01TemplateBody01(p):
	'''Extends01TemplateBody01 : empty 
								| Extends01 TemplateBody'''
	if len(p)==2:
		p[0] = Node("Extends01TemplateBody01", [p[1], p[2]], []).name
	else:
		p[0] = Node("Extends01TemplateBody01", [p[1]],[]).name

def p_Extends01(p):
	'''Extends01 : empty 
			  | Extends01 R_EXTENDS'''
	if len(p)==2:
		p[0] = Node("Extends01", [p[1]], [p[2]]).name
	else:
		p[0] = Node("Extends01", [p[1]],[]).name

def p_ClassTemplateOpt(p):
	''' ClassTemplateOpt : R_EXTENDS ClassTemplate
							| Extends01TemplateBody01'''
	if len(p)==2:
		p[0] = Node("ClassTemplateOpt", [p[2]], [p[1]]).name
	else:
		p[0] = Node("ClassTemplateOpt", [p[1]],[]).name

def p_ObjectDef(p):
	'ObjectDef : ID ClassTemplateOpt'
	p[0] = Node("ObjectDef", [p[2]], [p[1]]).name

def p_TraitDef(p):
	'TraitDef : ID TypeParamClause01 TraitTemplateOpt'
	p[0] = Node("TraitDef", [p[2], p[3]], [p[1]]).name

def p_TypeParamClause01(p):
	'''TypeParamClause01 : empty
					| TypeParamClause'''
	p[0] = Node("TypeParamClause01", [p[1]], []).name

def p_ClassDef(p):
	'ClassDef : ID TypeParamClause01 ConstrAnnotation01 AccessModifier01 ClassParamClauses ClassTemplateOpt'
	p[0] = Node("ClassDef", [p[2], p[3], p[4], p[5], p[5]], [p[1]]).name

def p_AccessModifier01(p):
	'''AccessModifier01 : empty 
						|  AccessModifier'''
	p[0] = Node("AccessModifier01", [p[1]], []).name

def p_ConstrAnnotation01(p):
	'''ConstrAnnotation01 : empty
							| ConstrAnnotation'''
	p[0] = Node("ConstrAnnotation01", [p[1]], []).name

def p_TmplDef(p):
	'''TmplDef : Case01 R_CLASS ClassDef
			| Case01 R_OBJECT ObjectDef
			| R_TRAIT TraitDef'''
	if "ClassDef" in p[3]:
		p[0] = Node("TmplDef", [p[1], p[3]], [p[2]]).name
	if "ObjectDef" in p[3]:
		p[0] = Node("TmplDef", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("TmplDef", [p[2]],[p[1]]).name

def p_Case01(p):
	'''Case01 : empty 
				| R_CASE'''
	if p[1] == "case":
		p[0] = Node("Case01", [], [p[1]]).name
	else:
		p[0] = Node("Case01", [p[1]], []).name

def p_TypeDef(p):
	'TypeDef : ID TypeParamClause01 EQUALASS Type'
	p[0] = Node("TypeDef", [p[2], p[4]], [p[1], p[3]]).name


def p_FunDef(p):
	'''FunDef : FunSig ColonType01 EQUALASS Expr
			| FunSig nl01 BLOCKOPEN Block BLOCKCLOSE
			| R_THIS ParamClause ParamClauses EQUALASS ConstrExpr
			| R_THIS ParamClause ParamClauses nl01 ConstrBlock'''
	if "ColonType01" in p[2]:
		p[0] = Node("FunDef", [p[1], p[2], p[4]], [p[3]]).name
	if "nl01" in p[2]:
		p[0] = Node("FunDef", [p[1], p[2], p[4]], [p[3], p[5]]).name
	if "nl01" in p[4]:
		p[0] = Node("FunDef", [p[2], p[3], p[4], p[5]], [p[1]]).name
	else:
		p[0] = Node("FunDef", [p[2], p[3], p[5]], [p[1], p[4]]).name

def p_ColonType01(p):
	'''ColonType01 : empty 
				| COLON Type'''
	if len(p):
		p[0] = Node("Case01", [], [p[1]]).name
	else:
		p[0] = Node("Case01", [p[1]], []).name
	
#check for nl
def p_nl01(p):
	'''nl01 : empty 
			| nl'''
	if "nl" in p[1]:
		p[0] = Node("nl01", [p[1]], []).name
	else:
		p[0] = Node("nl01", [], [p[1]]).name

#check for ids 
def p_VarDef(p):
	'''VarDef : PatDef
			| ids COLON Type EQUALASS UNDERSCORE'''
	if "Patdef" in p[1]:
		p[0] = Node("Vardef", [p[1]], []).name
	else:
		p[0] = Node("Vardef", [p[1], p[3]], [p[2], p[4], p[5]]).name

def p_PatDef(p):
	'PatDef : Pattern2 CommaPattern20more ColonType01 EQUALASS Expr'
	p[0] = Node("Patdef", [p[1], p[2], p[3], p[5]], [p[4]]).name

def  p_CommaPattern20more(p):
	'''CommaPattern20more : empty
						  | CommaPattern20more COMMA Pattern2'''
	if "CommaPatter20more" in p[1]:
		p[0] = Node("CommaPatter20more", [p[1], p[3]], [p[2]]).name
	else:
		p[0] = Node("CommaPatter20more", [p[1]], []).name

def p_Def(p):
	'''Def : ParVarDef
		| R_DEF FunDef
		| R_TYPE nl0more TypeDef
		| TmplDef'''
	if len(p)==4:
		p[0] = Node("Def", [p[2],p[3]],[p[1]]).name
	elif len(p)==3:
		p[0] = Node("Def", [p[2]], [p[1]]).name
	elif "ParVarDef" in p[1]:
		p[0] = Node("Def", [p[1]], []).name
	else
		p[0] = Node("Def", [p[1]],[]).name

def p_nl0more(p):
	'''nl0more : empty
				| nl0more nl '''
	if "nl0more" in p[1]:
		p[0] = Node("nl0more", [p[1], p[2]], []).name
	else:
		p[0] = Node("nl0more", [p[1]], []).name

def p_PatVarDef(p):
	'''PatVarDef : R_VAL PatDef
				| R_VAR VarDef'''
	if "PatDef" in p[2]:
		p[0] = Node("PatVarDef", [p[2]], [p[1]]).name
	else:
		p[0] = Node("PatVarDef", [p[2]], [p[1]]).name
#check for id
def p_TypeDcl(p):
	'TypeDcl : id TypeParamClause01 Obscure2Type01 ObscureType01'
	p[0] = Node("TypeDcl", [p[1], p[2], p[3], p[4]], []).name


def p_Obscure2Type01(p):
	'''Obscure2Type01 : empty 
					| R_OBSCURE2 Type'''
	if "Type" in p[2]:
		p[0] = Node("Obscure2Type01", [p[2]], [p[1]]).name
	else:
		p[0] = Node("Obscure2Type01", [p[1]], []).name

def p_ObscureType01(p):
	'''ObscureType01 : empty 
					| R_OBSCURE Type'''
	if "Type" in p[2]:
		p[0] = Node("ObscureType01", [p[2]], [p[1]]).name
	else:
		p[0] = Node("ObscureType01", [p[1]], []).name

def p_FunSig(p):
	'FunSig : id FunTypeParamClause01 ParamClauses'
	p[0] = Node("FunSig", [p[1], p[2], p[3]], []).name

def p_FunTypeParamClause01(p):
	''' FunTypeParamClause01 : empty 
							| FunTypeParamClause'''
	if "FunTypeParamClause" in p[2]:
		p[0] = Node("FunTypeParamClause01", [p[1]], []).name
	else:
		p[0] = Node("FunTypeParamClause01", [p[1]], []).name

def p_FunDcl(p):
	'FunDcl : FunSig ColonType01'
	p[0] = Node("FunDcl", [p[1], p[2]], []).name

def p_VarDcl(p):
	'VarDcl : ids COLON Type'
	p[0] = Node("VarDcl", [p[1], p[3]], [p[2]]).name

def p_ValDcl(p):
	'ValDcl : ids COLON Type'
	p[0] = Node("ValDcl", [p[1], p[3]], [p[2]]).name

def p_Dcl(p):
	'''Dcl : R_VAL ValDcl
		| R_VAR VarDcl
		| R_DEF FunDcl
		| R_TYPE nl0more TypeDcl'''
	if len(p)==4:
		p[0] = Node("Dcl", [p[2],p[3]],[p[1]]).name
	elif "FunDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	elif "VarDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	else
		p[0] = Node("Dcl", [p[2]],[p[1]]).name

def p_ImportSelector(p):
	'ImportSelector : id ImpliesidorUnderscore01'
	p[0] = Node("ImportSelector", [p[1], p[2]], []).name

def p_ImpliesidorUnderscore01(p):
	'''ImpliesidorUnderscore01 : empty 
							 | 	R_IMPLIES1 id
							| R_IMPLIES1 UNDERSCORE'''
	if len(p)==4:
		p[0] = Node("Dcl", [p[2],p[3]],[p[1]]).name
	elif "FunDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name
	elif "VarDcl" in p[2]:
		p[0] = Node("Dcl", [p[2]], [p[1]]).name

def p_ImportSelectors(p):
	'''ImportSelectors : BLOCKOPEN ImportselectorComma0more ImportSelector BLOCKCLOSE
					| BLOCKOPEN ImportselectorComma0more UNDERSCORE BLOCKCLOSE '''
	if "ImportSelector" in p[3]:
		p[0] = Node("ImportSelectors", [p[2], p[3]], [p[1], p[4]]).name
	else:
		p[0] = Node("ImportSelectors", [p[2]], [p[1], p[3], p[4]]).name

def p_ImportselectorComma0more(p):
	'''ImportselectorComma0more : empty
							| ImportselectorComma0more ImportSelector COMMA'''
	if "ImportSelector" in p[2]:
		p[0] = Node("ImportselectorComma0more", [p[1], p[2]], [p[3]]).name
	else:
		p[0] = Node("ImportselectorComma0more", [p[1]], []).name
	
def p_ImportExpr(p):
	'''ImportExpr : StableId DOT id
				| StableId DOT UNDERSCORE
				| StableId DOT ImportSelectors'''
	if "ImportSelectors" in p[3]:
		p[0] = Node("ImportExpr", [p[3],p[1]],[p[2]]).name
	elif "id" in p[3]:
		p[0] = Node("ImportExpr", [p[3], p[1]], [p[2]).name
	else:
		p[0] = Node("ImportExpr", [p[1], p[3]], [p[2]]).name

def p_Import(p):
	'Import : R_IMPORT ImportExpr CommaImportExpr0more'
	p[0] = Node("Import", [p[2], p[3]], [p[1]]).name
	
def p_CommaImportExpr0more(p):
	'''CommaImportExpr0more : empty
						| CommaImportExpr0more COMMA ImportExpr'''
	if "ImportExpr" in p[3]:
		p[0] = Node("CommaImportExpr0more", [p[1], p[3]], [p[3]]).name
	else:
		p[0] = Node("CommaImportExpr0more", [p[1]], []).name

def p_SelfType(p):
	'''SelfType : id ColonType01 R_IMPLIES1
			| R_THIS COLON Type R_IMPLIES1'''
	if "id" in p[1]:
		p[0] = Node("SelfType", [p[1], p[2]], [p[3]]).name
	else:
		p[0] = Node("SelfType", [p[3]], [p[1], p[2], p[4]).name

def p_TemplateStat(p):
	'''TemplateStat : TopStat1 Modifier0more Def
				| TopStat1 Modifier0more Dcl
				| Expr
				| empty'''
	if "Def" in p[3]:
		p[0] = Node("TemplateStat", [p[1], p[2],p[3]],[]).name
	elif "Def" in p[3]:
		p[0] = Node("TemplateStat", [p[1], p[2],p[3]],[]).name
	elif "Expr" in p[1]:
		p[0] = Node("TemplateStat", [p[1]], []).name
	else:
		p[0] = Node("TemplateStat", [p[1]], []).name

def p_TemplateBody(p):
	'TemplateBody : nl01 BLOCKOPEN SelfType01 TemplateStat semiTemplateStat0more BLOCKCLOSE'
	p[0] = Node("TemplateBody", [p[1], p[3], p[4], p[5]], [p[2], p[6]]).name
 
def p_semiTemplateStat0more(p):
	'''semiTemplateStat0more : empty
							| semiTemplateStat0more semi TemplateStat'''
	if "semi" in p[2]:
		p[0] = Node("semiTemplateStat0more", [p[1], p[2],p[3]],[]).name
	else
		p[0] = Node("semiTemplateStat0more", [p[1]],[]).name

def p_SelfType01(p):
	'''SelfType01 : empty
					| SelfType'''
	if "semi" in p[1]:
		p[0] = Node("SelfType01", [p[1]],[]).name
	else
		p[0] = Node("SelfType01", [p[1]],[]).name

def p_NameValuePair(p):
	'NameValuePair : R_VAL id EQUALASS PrefixExpr'
	p[0] = Node("NameValuePair", [p[2],p[4]],[p[1],p[3]]).name

def p_ConstrAnnotation(p):
	'ConstrAnnotation : R_ATTHERATE SimpleType ArgumentExprs'
	p[0] = Node("ConstrAnnotation", [p[2],p[3]],[p[1]]).name

def p_Annotation(p):
	'Annotation : R_ATTHERATE SimpleType ArgumentExprs0more'
	p[0] = Node("Annotation", [p[2],p[3]],[p[1]]).name

def p_AccessQualifier(p):
	'''AccessQualifier : LSQRB id RSQRB
					| LSQRB R_THIS RSQRB'''
	if "id" in p[2]:
		p[0] = Node("AccessQualifier", [p[2]],[p[1], p[3]]).name
	else
		p[0] = Node("AccessQualifier", [],[p[1], p[2], p[3]]).name

def p_AccessModifier(p):
	'''AccessModifier : R_PRIVATE AccessQualifier01
					| R_PROTECTED AccessQualifier01'''
	if p[1] == "private":
		p[0] = Node("AccessModifier", [p[2]],[p[1]]).name
	else
		p[0] = Node("AccessModifier", [p[2]],[p[1]]).name

def p_AccessQualifier01(p):
	'''AccessQualifier01 : empty
						| AccessQualifier'''
	if "AccessQualifier" in p[1]:
		p[0] = Node("AccessQualifier01", [p[1]],[]).name
	else
		p[0] = Node("AccessQualifier01", [p[1]],[]).name

def p_LocalModifier(p):
	'''LocalModifier : R_ABSTRACT
					| R_FINAL
					| R_SEALED
					| R_IMPLICIT
					| R_LAZY'''
	if p[1] == "abstract":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "final":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "sealed":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	if p[1] == "lazy":
		p[0] = Node("LocalModifier", [p[1]],[]).name
	else
		p[0] = Node("LocalModifier", [p[1]],[]).name

def p_Modifier(p):
	'''Modifier : LocalModifier
			| AccessModifier
			| R_OVERRIDE'''
	if "LocalModifier" in p[1]:
		p[0] = Node("Modifier", [p[1]],[]).name
	if "AccessModifier" in p[1]:
		p[0] = Node("Modifier", [p[1]],[]).name
	else
		p[0] = Node("Modifier", [],[p[1]]).name

def p_Binding(p):
	'''Binding : id ColonType01
			| UNDERSCORE ColonType01''' 
	if "id" in p[1]:
		p[0] = Node("Binding", [p[1],p[2]],[]).name
	else
		p[0] = Node("Binding", [p[2]],[p[1]]).name

def p_Bindings(p):
	'Bindings : LPARAN Binding CommaBinding0more RPARAN' 
	p[0] = Node("Bindings", [p[2],p[3]],[p[1], p[4]]).name

def p_CommaBinding0more(p):
	'''CommaBinding0more : empty
						| CommaBinding0more COMMA Binding'''
	if "Binding" in p[3]:
		p[0] = Node("CommaBinding0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaBinding0more", [p[1]],[]).name

def p_ClassParam(p):
	'ClassParam : Annotation0more Modifier0more valvar01 id  COLON ParamType EqualExpr01'
	p[0] = Node("ClassParam", [p[1], p[2],p[3], p[4], p[6], p[7]],[p[5]]).name

def p_Annotation0more(p):
	'''Annotation0more : empty
					| Annotation0more Annotation'''
	if "Annotation" in p[2]:
		p[0] = Node("Annotation0more", [p[1],p[2]],[]).name
	else:
		p[0] = Node("Annotation0more", [p[1]],[]).name

def p_valvar01(p):
	'''valvar01 : empty
			| R_VAL
			| R_VAR'''
	if p[1] == "val":
		p[0] = Node("valvar01", [p[1]],[]).name
	if p[1] == "var":
		p[0] = Node("valvar01", [p[1]],[]).name
	else:
		p[0] = Node("valvar01", [p[1]],[]).name

def p_EqualExpr01(p):
	'''EqualExpr01 : empty
				| EQUALASS Expr'''
	if "Expr" in p[2]:
		p[0] = Node("EqualExpr01", [p[2]],[p[1]]).name
	else:
		p[0] = Node("EqualExpr01", [p[1]],[]).name

def p_ClassParams(p):
	'ClassParams : ClassParam CommaClassParam0more'
	p[0] = Node("ClassParams", [p[1],p[2]],[]).name

def p_CommaClassParam0more(p):
	'''CommaClassParam0more : empty
						| CommaClassParam0more COMMA ClassParam'''
	if "Expr" in p[2]:
		p[0] = Node("CommaClassParam0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaClassParam0more", [p[1]],[]).name

def p_ClassParamClause(p):
	'ClassParamClause : nl01 LPARAN ClassParams01 RPARAN'
	p[0] = Node("ClassParamClause", [p[1],p[3]],[p[2], p[4]]).name

def p_ClassParams01(p):
	'''ClassParams01 : empty
					| ClassParams '''
	if "ClassParams" in p[1]:
		p[0] = Node("ClassParams01", [p[1]],[]).name
	else:
		p[0] = Node("ClassParams01", [p[1]],[]).name

def p_ClassParamClauses(p):
	'ClassParamClauses : ClassParamClause0more Temp01'
	p[0] = Node("ClassParamClauses", [p[1],p[2]],[]).name

def p_ClassParamClause0more(p):
	'''ClassParamClause0more : ClassParamClause0more ClassParamClause
								| empty'''

def p_Temp01(p):
	'''Temp01 : nl01 LPARAN R_IMPLICIT ClassParams RPARAN
			| empty'''
	if "ClassParams" in p[4]:
		p[0] = Node("Temp01", [p[1], p[4]],[p[2], p[3], p[5]]).name
	else:
		p[0] = Node("Temp01", [p[1]],[]).name

def p_ParamType(p):
	'''ParamType : Type
				| R_IMPLIES1 Type
				| Type MULASS'''
	if len(p)==1:
		p[0] = Node("ParamType", [p[1]],[]).name
	elif "Type" in p[2]:
		p[0] = Node("ParamType", [p[2]],[p[1]]).name
	else:
		p[0] = Node("ParamType", [p[1]],[p[2]]).name

def p_Param(p):
	'Param : Annotation0more id ColonParamType01 EqualExpr01'
	p[0] = Node("Param", [p[1], p[2], p[3], p[4]],[]).name

def p_ColonParamType01(p):
	'''ColonParamType01 : empty
					| COLON ParamType'''
	if "ParamType" in p[2]:
		p[0] = Node("ParamType", [p[2]],[p[1]]).name
	else:
		p[0] = Node("ParamType", [p[1]],[]).name

def p_Params(p):
	'Params : Param CommaParam0more'
	p[0] = Node("Params", [p[1], p[2]],[]).name

def p_CommaParam0more(p):
	'''CommaParam0more : empty
					| CommaParam0more COMMA Param'''
	if "Param" in p[3]:
		p[0] = Node("CommaParam0more", [p[1],p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaParam0more", [p[1]],[]).name

def p_ParamClause(p):
	'ParamClause : nl01 LPARAN Params01 RPARAN'
	p[0] = Node("ParamClause", [p[1],p[3]],[p[2],p[4]]).name

def p_Params01(p):
	'''Params01 : empty
			| Params'''
	if "Params" in p[1]:
		p[0] = Node("Params01", [p[1]],[]).name
	else:
		p[0] = Node("Params01", [p[1]],[]).name

def p_ParamClauses(p):
	'ParamClauses : ParamClause0more Temp02'
	p[0] = Node("ParamsClauses", [p[1], p[2]],[]).name

def p_ParamClause0more(p):
	'''ParamClause0more : empty
					| ParamClause0more ParamClause'''
	if "ParamClause0more" in p[1]:
		p[0] = Node("ParamClause0more", [p[1], p[2]],[]).name
	else:
		p[0] = Node("ParamClause0more", [p[1]],[]).name

def p_Temp02(p):
	'''Temp02 : nl01 LPARAN R_IMPLICIT Params RPARAN
			| empty'''
if "Params" in p[4]:
		p[0] = Node("Temp02", [p[1], p[4]],[p[2], p[3], p[5]]).name
	else:
		p[0] = Node("Temp02", [p[1]],[]).name

def p_TypeParam(p): 
	'''TypeParam : id  TypeParamClause01  Obscure2Type01 ObscureType01 ObscureType0more ColonType0more	
				| UNDERSCORE TypeParamClause01  Obscure2Type01 ObscureType01 ObscureType0more ColonType0more'''
	if "id" in p[1]:
		p[0] = Node("TypeParam", [p[1], p[2], p[3], p[4], p[5], p[6]],[]).name
	else:
		p[0] = Node("TypeParam", [p[2], p[3], p[4], p[5], p[6]],[p[1]]).name

def p_ObscureType0more(p):
	'''ObscureType0more : empty
						| ObscureType0more R_OBSCURE Type'''
	if "Type" in p[3]:
		p[0] = Node("ObscureType0more", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("ObscureType0more", [p[1]],[]).name

def p_ColonType0more(p):
	'''ColonType0more : empty
					| ColonType0more COLON Type'''
	if "Type" in p[3]:
		p[0] = Node("ColonType0more", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("ColonType0more", [p[1]],[]).name

def p_VariantTypeParam(p):
	'''VariantTypeParam : Annotation0more TypeParam
					| Annotation0more PLUS TypeParam
					| Annotation0more MINUS TypeParam'''
	if len(p)==4:
		p[0] = Node("VariantTypeParam", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("VariantTypeParam", [p[1], p[2]],[]).name

def p_FunTypeParamClause(p):
	'FunTypeParamClause : LSQRB TypeParam CommaTypeParam0more RSQRB'
	p[0] = Node("FunTypeParamClause", [p[2], p[3]],[p[1], p[4]]).name

def p_CommaTypeParam0more(p):
	'''CommaParam0more : empty
					| CommaTypeParam0more COMMA TypeParam'''
	if len(p)==4:
		p[0] = Node("CommaParam0more", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaParam0more", [p[1]],[]).name

def p_TypeParamClause(p):
	'TypeParamClause : LSQRB VariantTypeParam CommaVariantTypeParam0more RSQRB'
	p[0] = Node("TypeParamClause", [p[2], p[3]],[p[1], p[4]]).name

def p_CommaVariantTypeParam0more(p):
	'''CommaVariantTypeParam0more : empty
							| CommaVariantTypeParam0more COMMA VariantTypeParam''' 
	if len(p)==4:
		p[0] = Node("CommaVariantParam0more", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("CommaVariantParam0more", [p[1]],[]).name

#look reference there is ambiguity 
def p_Patterns(p):
	'Patterns : Pattern CommaPatterns01'

def p_CommaPatterns01(p):
	'''CommaPatterns01 : empty
					| COMMA Patterns'''
	if len(p)==3:
		p[0] = Node("CommaPatterns01", [p[2]],[p[1]]).name
	else:
		p[0] = Node("CommaPatterns01", [p[1]],[]).name
#look reference

def p_SimplePattern(p):
	'''SimplePattern : UNDERSCORE
					| varid
					| Literal
					| StableId
					| StableId LPARAN Patterns01 RPARAN
					| StableId LPARAN PatternsComma01 varidUnderscore01 UNDERSCORE MULTIPLICATION RPARAN
					| LPARAN Patterns01 RPARAN
					| XmlPattern'''
	if len(p)==8:
		p[0] = Node("SimplePattern", [p[1], p[3], p[4]],[p[2], p[5], p[6], p[7]]).name
	elif len(p)==5:
		p[0] = Node("SimplePattern", [p[1], p[3]],[p[2], p[4]]).name
	elif len(p)==4:
		p[0] = Node("SimplePattern", [p[2]],[p[1], p[3]]).name
	elif "XmlPattern" in p[1]:
		p[0] = Node("SimplePattern", [p[1]],[]).name
	elif "StableID" in p[1]:
		p[0] = Node("SimplePattern", [p[1]],[]).name
	elif "Literal" in p[1]:
		p[0] = Node("SimplePattern", [p[1]],[]).name
	elif "varid" in p[1]:
		p[0] = Node("SimplePattern", [p[1]],[]).name
	else:
		p[0] = Node("SimplePattern", [p[1]],[]).name

def p_Patterns01(p):
	'''Patterns01 : empty
				| Patterns'''
	if "Patterns" in p[1]:
		p[0] = Node("Patterns01", [p[1]],[p[1]]).name
	else:
		p[0] = Node("Patterns01", [p[1]],[]).name

def p_PatternsComma01(p):
	'''PatternsComma01 : empty
				| Patterns COMMA'''
	if len(p)==3:
		p[0] = Node("PatternsComma01", [p[1]],[p[2]]).name
	else:
		p[0] = Node("PatternsComma01", [p[1]],[]).name

def p_varidUnderscore01(p):
	'''varidUnderscore01 : empty
				| varid  UNDERSCORE'''
	if len(p)==3:
		p[0] = Node("varidUnderscore01", [p[1]],[p[2]]).name
	else:
		p[0] = Node("varidUnderscore01", [p[1]],[]).name

def p_Pattern3(p):
	'''Pattern3 : SimplePattern
			| SimplePattern idnl01SimplePattern0more'''
	if len(p)==3:
		p[0] = Node("Pattern3", [p[1], p[2]],[]).name
	else:
		p[0] = Node("Pattern3", [p[1]],[]).name

def p_idnl01SimplePattern0more(p):
	'''idnl01SimplePattern0more : empty
				| idnl01SimplePattern0more id nl01 SimplePattern'''
	if len(p)==5:
		p[0] = Node("idnl01SimplePattern0more", [p[1], p[2], p[3], p[4]],[]).name
	else:
		p[0] = Node("idnl01SimplePattern0more", [p[1]],[]).name

def p_Pattern2(p):
	'''Pattern2 : varid AttheratePattern301
		| Pattern3'''
	if len(p)==3:
		p[0] = Node("Pattern2", [p[1], p[2]],[]).name
	else:
		p[0] = Node("Pattern2", [p[1]],[]).name

def p_AttheratePattern301(p):
	'''AttheratePattern301 : empty
				| ATTHERATE Pattern3''' 
	if len(p)==3:
		p[0] = Node("AttheratePattern301", [p[2]],[p[1]]).name
	else:
		p[0] = Node("AttheratePattern301", [p[1]],[]).name

def p_Pattern1(p):
	'''Pattern1 : varid COLON TypePat
				| UNDERSCORE COLON TypePat
				| Pattern2'''
	if "varid" in p[1]:
		p[0] = Node("Pattern01", [p[1], p[3]],[p[2]]).name
	elif "Pattern2" in p[1]:
		p[0] = Node("Pattern01", [p[1]],[]).name
	else:
		p[0] = Node("Pattern01", [p[3]],[p[1],p[2]]).name

def p_Pattern(p):
	'Pattern : Pattern1  BitorPattern10more'
	p[0] = Node("Pattern", [p[1], p[2]],[]).name

def p_BitorPattern10more(p):
	'''BitorPattern10more : BitorPattern10more BITOR Pattern1
						| empty'''
	if len(p)==4:
		p[0] = Node("BitorPattern10more", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("BitorPattern10more", [p[1]],[]).name

def p_Guard(p):
	'Guard : R_IF PostfixExpr'
	p[0] = Node("Guard", [p[2]],[p[1]]).name

def p_CaseClause(p):
	'CaseClause : R_CASE Pattern Guard01 R_IMPLIES1 Block'
	p[0] = Node("CaseClause", [p[2], p[3], p[5]],[p[1], p[4]]).name

def p_Guard01(p):
	'''Guard01 : Guard
			| empty'''
	if "Guard" in p[1]:
		p[0] = Node("Guard", [p[1]],[]).name
	else:
		p[0] = Node("Guard", [p[1]],[]).name

def p_CaseClauses(p):
	'CaseClauses : CaseClause CaseClause0more'
	p[0] = Node("CaseClauses", [p[1], p[2]],[]).name

def p_CaseClause0more(p):
	'''CaseClause0more : empty
					| CaseClause0more CaseClause'''
	if "CaseClause0more" in p[1]:
		p[0] = Node("CaseClause0more", [p[1]],[p[2]]).name
	else:
		p[0] = Node("CaseClause0more", [p[1]],[]).name

def p_Generator(p):
	'Generator : Pattern1 R_LEFTARROW1 Expr Guard01'
	p[0] = Node("Generator", [p[1], p[3], p[4]],[p[2]]).name

def p_Enumerator(p):
	'''Enumerator : Generator
				| Guard
				| Pattern1 EQUALASS Expr''' 
	if "Pattern1" in p[1]:
		p[0] = Node("Enumerator", [p[1], p[3]],[p[2]]).name
	elif "Guard" in p[1]:
		p[0] = Node("Enumerator", [p[1]],[]).name
	else:
		p[0] = Node("Enumerator", [p[1]],[]).name

def p_Enumerators(p):
	'Enumerators ::= Generator semiEnumerator0more'
	p[0] = Node("Enumerators", [p[1], p[2]],[]).name

def p_semiEnumerator0more(p):
	'''semiEnumerator0more : empty
						| semiEnumerator0more semi Enumerator'''
	if "semiEnumerator" in p[1]:
		p[0] = Node("semiEnumerator0more", [p[1], p[2], p[3]],[]).name
	else
		p[0] = Node("semiEnumerator0more", [p[1]],[]).name

def p_ResultExpr(p):
	'''ResultExpr : Expr1
				| Bindings R_IMPLIES1 Block
				| UNDERSCORE COLON CompoundType R_IMPLIES1 Block
				|  R_IMPLICIT id  COLON CompoundType R_IMPLIES1 Block
				| id  COLON CompoundType R_IMPLIES1 Block'''
	if "id" in p[1]:
		p[0] = Node("ResultExpr", [p[1], p[3], p[5]],[p[2], p[4]]).name
	elif "id" in p[2]:
		p[0] = Node("ResultExpr", [p[2], p[4], p[6]],[p[1], p[3], p[5]]).name
	elif "CompoundType" in p[3]:
		p[0] = Node("ResultExpr", [p[3], p[5]],[p[1], p[2], p[4]]).name
	elif "Bindings" in p[1]:
		p[0] = Node("ResultExpr", [p[1], p[3]],[p[2]]).name
	else:
		p[0] = Node("ResultExpr", [p[1]],[]).name

#check Import	
def p_BlockStat(p):
	'''BlockStat : Import
				| Annotation0more  Def
				| Annotation0more R_IMPLICIT Def
				| Annotation0more  R_LAZY Def
				| Annotation0more LocalModifier0more TmplDef
				| Expr1
				| empty'''
	if "LocalModifier0more" in p[2]:
		p[0] = Node("BlockStat", [p[1], p[2], p[3]],[]).name
	elif "lazy" in p[2]:
		p[0] = Node("BlockStat", [p[1], p[3]],[p[2]]).name
	elif "Implicit" in p[2]:
		p[0] = Node("BlockStat", [p[1], p[3]],[p[2]]).name
	elif len(p)==2:
		p[0] = Node("BlockStat", [p[1], p[2]],[]).name
	elif "Import" in p[1]:
		p[0] = Node("BlockStat", [p[1]],[]).name
	elif "Expr1" in p[1]:
		p[0] = Node("BlockStat", [p[1]],[]).name
	else:
		p[0] = Node("BlockStat", [p[1]],[]).name

def p_LocalModifier0more(p):
	'''LocalModifier0more : empty
						| LocalModifier0more LocalModifier'''
	if len(p)==3:
		p[0] = Node("LocalModifier0more", [p[1], p[2]],[]).name
	else:
		p[0] = Node("LocalModifier0more", [p[1]],[]).name

def p_Block(p):
	'Block : BlockStatsemi0more ResultExpr01'
	p[0] = Node("Block", [p[1], p[2]],[]).name

def p_ResultExpr01(p):
	'''ResultExpr01 : empty	
					| ResultExpr'''
	if len(p)==3:
		p[0] = Node("ResultExpr01", [p[1]],[]).name
	else:
		p[0] = Node("ResultExpr01", [p[1]],[]).name

def p_BlockStatsemi0more(p):
	'''BlockStatsemi0more : BlockStatsemi0more BlockStat semi
							| empty'''
	if len(p)==4:
		p[0] = Node("BlockStatsemi0more", [p[1], p[2], p[3]],[]).name
	else:
		p[0] = Node("BlockStatsemi0more", [p[1]],[]).name

def p_BlockExpr(p):
	'''BlockExpr : BLOCKOPEN CaseClauses BLOCKCLOSE
				| BLOCKOPEN Block BLOCKCLOSE'''
	if "Block" in p[2]:
		p[0] = Node("BlockExpr", [p[2]],[p[1], p[3]]).name
	else:
		p[0] = Node("BlockExpr", [p[2]],[p[1], p[3]]).name
def p_ArgumentExprs(p):
	'''ArgumentExprs : LPARAN Exprs RPARAN
					| LPARAN RPARAN
					| LPARAN ExprsComma01 PostfixExpr COLON UNDERSCORE MULTIPLICATION RPARAN
					| nl01 BlockExpr'''
	if "nl01" in p[1]:
		p[0] = Node("ArgumentExprs", [p[1], p[2]],[]).name
	elif "ExprsComma01" in p[2]:
		p[0] = Node("ArgumentExprs", [p[2], p[3]],[p[1], p[4], p[5], p[6], p[7]]).name
	elif "Exprs" in p[2]:
		p[0] = Node("ArgumentExprs", [p[2]],[p[1],p[3]]).name
	else:
		p[0] = Node("ArgumentExprs", [], [p[1],p[2]])

def p_ExprsComma01(p):
	'''ExprsComma01 : empty
					| Exprs COMMA'''
	if "Exprs" in p[1]:
		p[0] = Node("ExprsComma01", [p[1]],[p[2]]).name
	else:
		p[0] = Node("ExprsComma01", [p[1]]).name



def p_Ids(p):
        "Ids : ID "
        if(len(p) == 2):
                p[0] = Node("Ids", None, [p[1]] )
        else:
                p[0] = Node("Ids", [p[3]], [p[1],p[2]])



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


def p_empty(p):
    'empty :'
    pass
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
