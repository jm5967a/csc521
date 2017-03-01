import pprint

pp = pprint.PrettyPrinter(indent=1, depth=10)

tokens = ["VAR", "IDENT:X", "COMMA", 'VAR', "IDENT Y", "ASSIGN", "IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
tokens = ["VAR", "IDENT:X", "ASSIGN", "IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
tokens = ["Print", "NUMBER:9", "ADD", "NUMBER:9", 'EOF']


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
def FunctionDec(token_index):
    pass


def Prints(token_index):
    token_index += 1
    print(tokens[token_index])
    (success, returned_index, returned_subtree) = Expression(token_index)
    if success:
        subtree = ["Prints ", returned_subtree]
        print(subtree)


def Namelist(token_index):
    '''
    <NameList> -> <Name> COMMA <NameList> | <Name>
    '''
    if tokens[token_index] == 'VAR':
        token_index += 1
        (success, returned_index, returned_subtree) = Name(token_index)
        subtree = returned_subtree
        if success:
            token_index += 1
            while tokens[token_index] == "COMMA" and 'VAR' == tokens[token_index + 1]:
                token_index += 2
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
pp.pprint(Prints(0))
