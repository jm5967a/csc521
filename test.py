import pprint

pp = pprint.PrettyPrinter(indent=1, depth=100)

tokens = ["VAR", "IDENT:X", "COMMA", 'VAR', "IDENT Y", "ASSIGN", "IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
tokens = ["VAR", "IDENT:X", "ASSIGN", "IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
tokens = ["Print", "NUMBER:9", "ADD", "NUMBER:9", 'EOF']
tokens = ["FUNCTION", "IDENT:X", "LPAREN", "IDENT:Y", 'COMMA', 'IDENT:K', "RPAREN", "EOF"]
# tokens = ["FUNCTION", "IDENT:X", "LPAREN", "IDENT:Y", 'COMMA', 'IDENT:K', "RPAREN", "LBRACE", 'RETURN', 'RBRACE', 'VAR',
#  "IDENT:T", 'ASSIGN', 'NUMBER:2','PRINT','NUMBER:2', 'EOF']
tokens = ["FUNCTION", "IDENT:X", "LPAREN", "IDENT:Y", 'COMMA', 'IDENT:K', "RPAREN", "LBRACE", 'RETURN', 'IDENT:yk',
          'RBRACE', 'VAR',
          "IDENT:T", 'ASSIGN', 'NUMBER:2', 'EOF']
file = open("testfile.txt", "r")
tokens = file.read().split(",")
tokens[len(tokens) - 1] = "EOF"


# tokens = ["SUB", "IDENT:X", "ADD", "NUMBER:4"]
# tokens = ["SUB", "IDENT:X", "EXP", "NUMBER:4", "EOF"]
# tokens = ["SUB", "IDENT:X", "EXP", "NUMBER:4", "EXP", "IDENT:X", "EOF"]
# tokens = ["NUMBER:9", "DIV", "IDENT:X", "EXP",
#           "NUMBER:4", "EXP", "IDENT:X", "EOF"]
# tokens = ["NUMBER:9", "ADD", "IDENT:X", "SUB", "NUMBER:4", "EOF"]
# tokens = ["NUMBER:9", "ADD", "LPAREN", "IDENT:X",
#           "SUB", "NUMBER:4", "RPAREN", "EOF"]
# tokens = ["LPAREN", "IDENT:X", "SUB", "NUMBER:4", "RPAREN", "EOF"]
# tokens = ["IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
# tokens = ["IDENT:FOO", "LPAREN", "RPAREN", "COLON", "NUMBER:0", "EOF"]
# tokens=["VAR", "IDENT:X"]
# tokens = ["SUB", "IDENT:X", "EOF"]

# begin utilities
def is_ident(tok):
    '''Determines if the token is of type IDENT.
    tok - a token
    returns True if IDENT is in the token or False if not.
    '''

    return -1 < tok.find("IDENT")


def is_number(tok):
    '''Determines if the token is of type NUMBER.
    tok - a token
    returns True if NUMBER is in the token or False if not.
    '''
    return -1 < tok.find("NUMBER")


# end utilities
final = []


def Program():
    pass


def Statement(token_index):
    returned_index = 0

    while returned_index + 1 != len(tokens):

        (success, returned_index, returned_subtree) = FunctionDec(returned_index)
        if success:
            final.append(["Statement", returned_subtree])
            returned_index += 1
        else:
            (success, returned_index, returned_subtree) = Assignment(returned_index)
            if success:
                final.append(["Statement", returned_subtree])
            (success, returned_index, returned_subtree) = Prints(returned_index)
            if success:
                final.append(["Statement", returned_subtree])
                print(tokens[returned_index])
        if returned_index == 0:
            raise Exception("Syntax Error")



    return final


def Param(token_index):
    # < ParameterList > -> < Parameter > COMMA < ParameterList > | < Parameter >
    # < Parameter > -> < Expression > | < Name >
    subtree = []

    def Parameter(token_index):
        token_index += 1
        (success, returned_index, returned_subtree) = Expression(token_index)
        if success:
            subtree = ['Parameter', returned_subtree]
            return [True, returned_index, subtree]
        (success, returned_index, returned_subtree) = Name(token_index)
        if success:
            subtree = ['Parameter', returned_subtree]
            return [True, returned_index, subtree]
        return [False, token_index, []]

    (success, returned_index, returned_subtree) = Parameter(token_index)

    if success:
        returned_index += 1

        if 'COMMA' == tokens[returned_index]:
            while tokens[returned_index] == 'COMMA':
                returned_index += 1
                (success, returned_index, returned_subtree) = Parameter(token_index)
                subtree.append(returned_subtree)
                returned_index += 1
            return [True, returned_index, subtree]
        subtree = ['Parameter List', returned_subtree]

        return [True, returned_index, subtree]
    return [False, token_index, []]

def Return(token_index):
    (success, returned_index, returned_subtree) = Param(token_index)
    if success:
        subtree = ["RETURN", returned_subtree]
        return [True, returned_index, subtree]
    return [False, token_index, []]




def Functionbody(token_index):
    # need program function
    if tokens[token_index] == 'RETURN':
        (success, returned_index, returned_subtree) = Return(token_index)
        token_index += 1
        returned_index = token_index
        subtree = ['Function Body', returned_subtree]
        return [True, returned_index, subtree]
    return [False, token_index, []]


def Functionparam(token_index):
    if ("RPAREN" == tokens[token_index]):
        subtree = ["FunctonParams"]
        returned_index = token_index + 1
        return [True, returned_index, subtree]
    (success, returned_index, returned_subtree) = Namelist(token_index)
    if success:
        subtree = ["FunctonParams", returned_subtree]
        returned_index += 1
        return [True, returned_index, subtree]
    return [False, token_index, []]

    # subtree = ["FunctonParams", returned_subtree]


def FunctionDec(token_index):
    if 'FUNCTION' == tokens[token_index]:
        token_index += 1
        (success, returned_index, returned_subtree) = Name(token_index)
        if success:
            subtree = returned_subtree
            token_index += 1
            if "LPAREN" == tokens[token_index]:
                token_index += 1
                (success, returned_index, returned_subtree) = Functionparam(token_index)
                if success:
                    subtree = subtree, returned_subtree

                    token_index = returned_index
                    if 'LBRACE' == tokens[token_index]:
                        token_index += 1
                        (success, returned_index, returned_subtree) = Functionbody(token_index)

                        if success:
                            returned_index += 1
                            if "RBRACE" == tokens[returned_index]:
                                subtree = ['FunctionDeclaration', subtree, returned_subtree]
                                return [True, returned_index, subtree]
    return [False, token_index, []]


def Prints(token_index):
    if ("PRINT" == tokens[token_index]):
        token_index += 1
        (success, returned_index, returned_subtree) = Expression(token_index)
        if success:
            subtree = ["Prints ", returned_subtree]

            return [True, returned_index, subtree]

    return [False, token_index, []]


def Namelist(token_index):
    '''
    <NameList> -> <Name> COMMA <NameList> | <Name>
    '''
    (success, returned_index, returned_subtree) = Name(token_index)
    subtree = returned_subtree
    if success:
        token_index += 1
        while tokens[token_index] == "COMMA":
            token_index += 1
            (success, returned_index, returned_subtree) = Name(token_index)
            if success:
                token_index += 1
                subtree = subtree, returned_subtree

            else:
                raise Exception("Namelist Error")
        subtree = ["Namelist", subtree]
        return [True, returned_index, subtree]

    return [False, token_index, []]


def Assignment(token_index):
    def SingleAssignment(token_index):
        if 'VAR' == tokens[token_index] and tokens[token_index + 2] == 'ASSIGN' and is_ident(tokens[token_index + 1]):
            token_index += 3
            (success, returned_index, returned_subtree) = Expression(token_index)
            if success:
                subtree = ["SingleAssignment", returned_subtree]
                return [True, returned_index, subtree]
        return [False, token_index, []]

    def MultipleAssignment(token_index):
        # <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
        if 'VAR' == tokens[token_index]:
            (success, returned_index, returned_subtree) = Namelist(token_index)
            subtree = returned_subtree
            if success and 'ASSIGN' == tokens[returned_index]:
                returned_index += 1
                (success, returned_index, returned_subtree) = FunctionCall(returned_index)
                if success:
                    subtree = ["MultipleAssignment", subtree, returned_subtree]
                    return [True, returned_index, subtree]
        return [False, token_index, []]

    (success, returned_index, returned_subtree) = SingleAssignment(token_index)
    if success:
        subtree = ["Assignment0", returned_subtree]
        return [True, returned_index, subtree]

    (success, returned_index, returned_subtree) = MultipleAssignment(token_index)
    if success:
        subtree = ["Assignment1", returned_subtree]
        return [True, returned_index, subtree]
    return [False, token_index, []]

def Expression(token_index):
    '''<Expression> ->
        <Term> ADD <Expression>
        | <Term> SUB <Expression>
        | <Term>
    '''
    # <Term> ADD <Expression>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        subtree = ["Expression0", returned_subtree]
        if "ADD" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term> SUB <Expression>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        subtree = ["Expression1", returned_subtree]
        if "SUB" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        return [True, returned_index, ["Expression2", returned_subtree]]
    return [False, token_index, []]


def Term(token_index):
    '''<Term> ->
        <Factor> MULT <Term>
        | <Factor> DIV <Term>
        | <Factor>
    '''
    # <Factor> MULT <Term>
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term0", returned_subtree]
        if "MULT" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor> DIV <Term>
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term1", returned_subtree]
        if "DIV" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor>
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        return [True, returned_index, ["Term2", returned_subtree]]
    return [False, token_index, []]


def Factor(token_index):
    '''
    <Factor> ->
        <SubExpression>
        | <SubExpression> EXP <Factor>
        | <FunctionCall>
        | <Value> EXP <Factor>
        | <Value>
    '''
    # <SubExpression> EXP <Factor>
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor0", returned_subtree]
        if "EXP" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <SubExpression>
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor1", returned_subtree]
        return [True, returned_index, subtree]
    # <FunctionCall>
    (success, returned_index, returned_subtree) = FunctionCall(token_index)
    if success:
        return [True, returned_index, ["Factor2", returned_subtree]]
    # <Value> EXP <Factor>
    (success, returned_index, returned_subtree) = Value(token_index)
    if success:
        subtree = ["Factor3", returned_subtree]
        if "EXP" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Value>
    (success, returned_index, returned_subtree) = Value(token_index)
    if success:
        return [True, returned_index, ["Factor4", returned_subtree]]
    return [False, token_index, []]


def FunctionCall(token_index):
    '''
    <FunctionCall> ->
        <Name> LPAREN <FunctionCallParams> COLON <Number>
        | <Name> LPAREN <FunctionCallParams>
    '''
    # <Name> LPAREN <FunctionCallParams> COLON <Number>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:

        subtree = ["FunctionCall0", returned_subtree]
        if "LPAREN" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = FunctionCallParams(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                if "COLON" == tokens[returned_index]:
                    subtree.append(tokens[returned_index])
                    (success, returned_index, returned_subtree) = Number(
                        returned_index + 1)
                    if success:
                        subtree.append(returned_subtree)
                        return [True, returned_index, subtree]

                        # <Name> LPAREN <FunctionCallParams>
        (success, returned_index, returned_subtree) = Name(token_index)
        if success:
            subtree = ["FunctionCal1", returned_subtree]
            if "LPAREN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                (success, returned_index, returned_subtree) = FunctionCallParams(
                    returned_index + 1)
                if success:
                    subtree.append(returned_subtree)
                    return [True, returned_index, subtree]
    return [False, token_index, []]


def FunctionCallParams(token_index):
    '''
    <FunctionCallParams> ->
        <ParameterList> RPAREN
        | RPAREN
    '''
    # <ParameterList> RPAREN
    # todo after ParameterList is finished
    # RPAREN
    (success, returned_index, returned_subtree) = Param(token_index)
    if "RPAREN" == tokens[token_index]:
        subtree = ["FunctionCallParams1", tokens[token_index]]
        return [True, token_index + 1, subtree]
    return [False, token_index, []]


def SubExpression(token_index):
    '''<SubExpression> ->
        LPAREN <Expression> RPAREN
    '''
    if "LPAREN" == tokens[token_index]:
        subtree = ["SubExpression0", tokens[token_index]]
        (success, returned_index, returned_subtree) = Expression(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            if "RPAREN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                return [True, returned_index + 1, subtree]
    return [False, token_index, []]


def Value(token_index):
    '''
    <Value> ->
        <Name>
        | <Number>
    '''
    # try in order!
    # <name>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        return [True, returned_index, ["Value0", returned_subtree]]
    # <number>
    (success, returned_index, returned_subtree) = Number(token_index)
    if success:
        return [True, returned_index, ["Value1", returned_subtree]]
    return [False, token_index, []]


def Name(token_index):
    '''<Name> ->
        IDENT
        | SUB IDENT
        | ADD IDENT
    '''
    subtree = []
    if is_ident(tokens[token_index]):
        subtree = ["Name0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    if "SUB" == tokens[token_index]:
        if is_ident(tokens[token_index + 1]):
            subtree = ["Name1", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    if "ADD" == tokens[token_index]:
        if is_ident(tokens[token_index + 1]):
            subtree = ["Name2", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    return [False, token_index, subtree]


def Number(token_index):
    '''<Number> ->
        NUMBER
        | SUB NUMBER
        | ADD NUMBER
    '''
    subtree = []
    if is_number(tokens[token_index]):
        subtree = ["Number0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    if "SUB" == tokens[token_index]:
        if is_number(tokens[token_index + 1]):
            subtree = ["Number1", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    if "ADD" == tokens[token_index]:
        if is_number(tokens[token_index + 1]):
            subtree = ["Number2", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    return [False, token_index, subtree]


if __name__ == '__main__':
    print("starting __main__")
    x = Statement(0)
    pp.pprint(x)
