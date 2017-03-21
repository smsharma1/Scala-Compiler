Use following commands to run:

```
#!bash

$ cd /src
$ make
$ cd ..
$ ./bin/parser.py ./test/test1.scala (to execute the lexer on test-case file test1.scala)
```
Note that, at this point of time, we cannot look for functions declared in built in libraries of scala.

Following is the source of our grammar:
https://users-cs.au.dk/amoeller/RegAut/JavaBNF.html