# ProgramLang_HW1

Basic Lexer, Parser and Interpreter for the Quirk Language. The code is designed to be run on Python 2.7, but it can
be easily modified to run on 3.4/3.5 by changing raw_input() to input() in each file. Each file is capable of running
independently, but the input must be json encoded if you are attempting to run the interpreter. Examples 4 and 5 don't
work fully on the parser because of an error with multiple assignments.

Instructions to run:
On terminal with piping

(NOTE: LEXER INPUT MUST BE SEPARATED BY SPACES NOT NEW LINES (IE-- print 2 not print\n2)
Make a .txt file with the desired input. I named it passthrough.txt, but it could be called anything.
python Lexer.py < passthrough.txt | python Parser.py| python Interpreter.py

If you wanted to run the Lexer independently:
python Lexer.py
then type in desired input

If you wanted to run Parser independently:
python Parser.py
then type in desired input (The tokens must be separated by commas)


If you wanted to run Interpreter independently:
python Interpreter.py
then type in desired input



The Language grammar is below:
<Program> -> <Statement> <Program> | <Statement>

<Statement> -> <FunctionDeclaration> | <Assignment> | <Print>


//function declaration statements
<FunctionDeclaration> -> FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE

<FunctionParams> -> <NameList> RPAREN | RPAREN

<FunctionBody> -> <Program> <Return> | <Return>

<Return> -> RETURN <ParameterList>


//Assignment statements
<Assignment> -> <SingleAssignment> | <MultipleAssignment>

<SingleAssignment> -> VAR <Name> ASSIGN <Expression>


//size of NameList has to match the number of return values from the FunctionCall
<MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>


//print statements
<Print> -> PRINT <Expression>


//name and parameter list
<NameList> -> <Name> COMMA <NameList> | <Name>

<ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>

<Parameter> -> <Expression> | <Name>


//arithmetic expressions
<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>

<Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>

<Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>

<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>

<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN

<SubExpression> -> LPAREN <Expression> RPAREN

<Value> -> <Name> | <Number>


//Literals
<Name> -> IDENT | SUB IDENT | ADD IDENT

<Number> -> NUMBER | SUB NUMBER | ADD NUMBER
