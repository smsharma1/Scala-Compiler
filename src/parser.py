import ply.lex as lex
from ply.lex import TOKEN

tokens = (
	'INT',
	'FLOAT',
	'STRINTG',
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
    	'CHAR',         #Character
	'ID',           #Identifirs
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
	
)

t_DIGIT = r'[0-9]'
t_CHAR = r'[a-zA-Z]'

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'
@TOKEN(identifier)
def t_ID(t):
	return t

t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_INT = r'[+-]?([0-9])+'
t_FLOAT = r'([+-])?[0-9]+(\.[0-9]+)?'
t_BITWISE = r'([])'
t_LPARAN = r'\('
t_RPARAN = r'\)'
t_LSQRB = r'\['
t_RSQRB = r'\]'
t_BLOCKOPEN = r'\{'
t_BLOCKCLOSE = r'\}'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_MODULUS = r'%'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_AND = r'&&'
t_OR = r'||'
t_NOT = r'!'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

# Test it out
data = '''+10-9><>=<=-5.8'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
