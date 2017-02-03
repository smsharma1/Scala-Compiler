import ply.lex as lex

tokens = (
	'INT',
	'FLOAT',
	'STRINTG',
	'LPARAN',
	'RPARAN',
	'GE',
	'G',
	'LE',
	'L',
	'ID',           #Identifirs
	'NL',	        #Newline
	'ILT',	        #Integer literals
	'FLT',          #floating
	'BLT',		#boolean
	'CLT',		#Character
	'SLT',		#String
	'MSLT',		#multiline string
	'ES',		#escape sequence
	'SL',		#symbol literals
	'WAC',		#white spaces and comments
	'XML',		#XML
)

