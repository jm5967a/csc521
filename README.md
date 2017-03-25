# ProgramLang_HW1

Basic Lexer, Parser and Interpreter for the Quirk Lanuage. 
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
