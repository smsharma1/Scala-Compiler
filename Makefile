all: dir 

dir: mkdir cplex cpparse cpsymboltab binlex binparse binsymboltable

mkdir:
	mkdir bin

cplex:
	cp src/lexer.py bin/lexer.py

cpparse:
	cp src/parser.py bin/parser.py

cpsymboltab:
	cp src/symboltable.py bin/symboltable.py

binlex:
	chmod +x bin/lexer.py

binparse:
	chmod +x bin/parser.py 

binsymboltable:
	chmod +x bin/symboltable.py

clean:
	rm -r bin

clean-src:
	rm src/parser.out src/parse3.py src/*.png src/parsetab.py src/*.pyc src/*dot
clean-tests:
	rm tests/*dot
