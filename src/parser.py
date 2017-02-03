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
	'NL',	        #Newline
	'ILT',	        #Integer literals
	'FLT',          #floating
	'BLT',		#boolean
	'SLT',		#String
	'MSLT',		#multiline string
	'ES',		#escape sequence
	'SL',		#symbol literals
	'WAC',		#white spaces and comments
	'XML',		#XML
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
t_FLOAT = r'([+-])?[0-9]+[.]([0-9]+)?'
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


# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

# Test it out
data = '''+10-9><>=<=-5+=-=+=^^=>>>'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
