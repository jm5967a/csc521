Basic Lexer, Parser and Interpreter for the Quirk Language. The code is written in Clojure using the Leiningen tool. The code is deigned to be run through command line, but could be adapted to run through a tool like eclipse by removing the standard input variables. There are also two ways of running the program through command line, the first is just with the regular command lein run < “piped file”, which would return an interpreted result. The other way is with “pt” placed after lein run, this will output just the parse tree. 
Instructions to run: On terminal with piping


Interpreted version:
Lein run < Example.txt


Parse Tree Version:
Lein run -pt < Example.txt




The Language grammar is below: -> |
-> | |
//function declaration statements -> FUNCTION LPAREN LBRACE RBRACE
-> RPAREN | RPAREN
-> |
-> RETURN
//Assignment statements -> |
-> VAR ASSIGN
//size of NameList has to match the number of return values from the FunctionCall -> VAR ASSIGN
//print statements -> PRINT
//name and parameter list -> COMMA |
-> COMMA |
-> |
//arithmetic expressions -> ADD | SUB |
-> MULT | DIV |
-> EXP | | | EXP |
-> LPAREN COLON | LPAREN
-> RPAREN | RPAREN
-> LPAREN RPAREN
-> |
//Literals -> IDENT | SUB IDENT | ADD IDENT
-> NUMBER | SUB NUMBER | ADD NUMBER

