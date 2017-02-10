all: dir 

dir: mkdir cplex cpparse binlex binparse

mkdir:
	mkdir bin

cplex:
	cp src/lexer.py bin/lexer.py

cpparse:
	cp src/parser.py bin/parser.py

binlex:
	chmod +x bin/lexer.py

binparse:
	chmod +x bin/parser.py 

clean:
	rm -r bin
