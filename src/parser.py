import ply.lex as lex
from ply.lex import TOKEN

reserved = {
	'abstract' : 'R_ABSTRACT',
	'do'  : 'R_DO',
	'finally' : 'R_FINALLY',
	'import' : 'R_IMPORT',
	'object' : 'R_OBJECT',
	'override' : 'R_OVERRIDE',
	'package' : 'R_PACKAGE',
	'private' : 'R_PRIVATE',
	'protected' : 'R_PROTECTED',
	'return' : 'R_RETURN',
	'sealed' : 'R_SEALED',
 	'super' : 'R_SUPER',
	'this' : 'R_THIS',
	'throw' : 'R_THROW',
	'trait' : 'R_TRAIT',
	'try' : 'R_TRY',
	'true' : 'R_TRUE',
	'type' : 'R_TYPE', 
	'val' : 'R_VAL', 
	'var' : 'R_VAR', 
	'while' : 'R_WHILE',  
	'with' : 'R_WITH',
	'yield' : 'R_YIELD',
	'case' :'R_CASE',
	'catch' : 'R_CATCH',
	'class' : 'R_CLASS',
	'def' : 'R_DEF',
 	'else' : 'R_ELSE',
 	'extends' : 'R_EXTENDS',
 	'false' : 'R_FALSE', 
	'final' : 'R_FINAL',
 	'for' : 'R_FOR',
	'forSome' : 'R_FORSOME',
	'if' : 'R_IF',
	'implicit' : 'R_IMPLICIT',
 	'lazy' : 'R_LAZY',
	'match' : 'R_MATCH',
	'new' : 'R_NEW', 
	'null' : 'R_NULL',
	'\u21D2' : 'R_IMPLIES',
	'\u2190' : 'R_LEFTARROW',
	'_' : 'R_UNDERSCORE',
	':' : 'R_COLON',
	'=>' : 'R_IMPLIES1',
	'<-' : 'R_LEFTARROW1',
	'<:' : 'R_OBSCURE',
	'#' : 'R_HASH',
	'@' : 'R_ATTHERATE',
	'<%' : 'R_OBSCURE1',
	'>:' : 'R_OBSCURE2',
	'Byte' : 'R_BYTE',
	'Short' : 'R_SHORT',
	'Int' : 'R_INT',
	'Long' : 'R_LONG',
	'Float' : 'R_FLOAT',
	'Double' : 'R_DOUBLE',
	'Char' : 'R_CHAR',
	'String' : 'R_STRING',
	'Boolean' : 'R_BOOLEAN',
	'Unit' : 'R_UNIT',
	'Null' : 'R_NULL1',
	'Nothing' : 'R_NOTHING',
	'Any' : 'R_ANY',
	'AnyRef' : 'R_ANYREF'
}

tokens =list(reserved.values()) +  [
	'INT',
	'FLOAT',
	'LPARAN',
	'RPARAN',
	'LSQRB',
	'RSQRB',
	'BLOCKOPEN',
	'BLOCKCLOSE',
	'GT',           #Greater than
	'GE',           #Grearer than equal
	'LT',           #Less than
	'LE',           #Less than equal
	'DIGIT',        #Digit
    	'ID',
	'BITAND',
	'BITOR',
	'BITXOR',
	'BITNEG',
	'BITLSHIFT',
	'BITRSHIFT',
	'BITRSFILL',    #bit right shift fill operator
	'EQUALASS',
	'ADDASS',
	'SUBASS',
	'MULASS',
	'MODASS',
	'DIVASS',
	'BITLEFTASS',
	'BITRIGHTASS',
	'BITANDASS',
	'BITORASS',
	'BITXORASS',
	'PLUS',
	'MINUS',
	'MULTIPLICATION',
	'DIVISION',
	'MODULUS',
	'EQUAL',
	'NOTEQUAL',
	'AND',
	'OR',
	'NOT',
	'BACKSPACE',
	'HORITAB',
	'LINEFEED',
	'FORMFEED',
	'CARRIAGERETN',
	'DOUBLEQUOTE',
	'SINGLEQUOTE',
	'BACKSLASH',
]
digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'
@TOKEN(identifier)
def t_ID(t):
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t

t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_INT = r'[+-]?([0-9])+'
t_FLOAT = r'([+-])?[0-9]+\.([0-9]+)?'
t_LPARAN = r'\('
t_RPARAN = r'\)'
t_LSQRB = r'\['
t_RSQRB = r'\]'
t_BLOCKOPEN = r'\{'
t_BLOCKCLOSE = r'\}'
t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNEG = r'~'
t_BITLSHIFT = r'<<'
t_BITRSHIFT = r'>>'
t_BITRSFILL = r'>>>'
t_EQUALASS = r'='
t_ADDASS = r'\+='
t_SUBASS = r'-='
t_MULASS = r'\*='
t_MODASS = r'%='
t_DIVASS = r'/='
t_BITLEFTASS = r'<<='
t_BITRIGHTASS = r'>>='
t_BITANDASS = r'&='
t_BITORASS = r'\|='
t_BITXORASS = r'\^='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_MODULUS = r'%'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_BACKSPACE = r'\\b'
t_HORITAB = r'\t'
t_LINEFEED = r'\n'
t_FORMFEED = r'\f'
t_CARRIAGERETN = r'\r'
t_DOUBLEQUOTE = r'\"'
t_SINGLEQUOTE = r'\''
t_BACKSLASH = r'\\'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

# Test it out
data = '''+10-9"><>=<="'-5.8'+-/%==!=&&\||!\rwhile\tnew\n=>'''
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
