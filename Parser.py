import json
import pprint

pp = pprint.PrettyPrinter(indent=1, depth=300)


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
temp = []


def Program(index, function):
    global final

    (success, returned_index, returned_subtree) = Statement(index, function)
    if returned_index + 1 != len(tokens) and success:
        return True, returned_index, temp
    if success:
        done = ""

    x = 0
    done = ['Program0']
    if (len(
            final) < 2):  # if the final arrays contains more than substrings it will be program0 and if not it will be program1
        done = ['Program1']
    else:
        done = ['Program0']
    while x < len(
            final):  # loop to get the correct formatting for the parser--Append to final array
        if x == 0:
            done.append(final[x])
        else:
            done.append(["Program1", final[x]])
        x += 1

    return done  # return final array


def Statement(returned_index,
              function):  # main function to break off to specific functions--Function Declaration,assignment, print
    global final

    while returned_index + 1 != len(
            tokens):  # setup loop to continue until reachs last token
        (success, returned_index, returned_subtree) = FunctionDec(
            returned_index)

        if success:

            if function != 1:
                final.append(["Statement0",
                              returned_subtree])  # primary code to add tree to final array

                returned_index += 1
            else:
                temp.append(
                    ["Statement0", returned_subtree])  # funtion body utility
        else:
            (success, returned_index, returned_subtree) = Assignment(
                returned_index)
            if success:

                if function != 1:
                    final.append(["Statement1",
                                  returned_subtree])  # primary code to add tree to final array
                else:
                    temp.append(["Statement1",
                                 returned_subtree])  # funtion body utility
            (success, returned_index, returned_subtree) = Prints(
                returned_index)
            if success:
                if function != 1:
                    final.append(["Statement2",
                                  returned_subtree])  # primary code to add tree to final array

                else:
                    temp.append(["Statement2",
                                 returned_subtree])  # funtion body utility
            if tokens[returned_index] == "RETURN":
                return True, returned_index, final

    return [True, returned_index, final]


def Param(token_index):  # function that includes parameter and paramerterlist
    # < ParameterList > -> < Parameter > COMMA < ParameterList > | < Parameter >
    # < Parameter > -> < Expression > | < Name >
    subtree = []

    def Parameter(token_index):
        token_index += 1
        (success, returned_index, returned_subtree) = Expression(
            token_index)  # try to run token string through expression function and return tree
        if success:
            subtree = ['Parameter0', returned_subtree]
            return [True, returned_index, subtree]
        (success, returned_index, returned_subtree) = Name(
            token_index)  # try to run token string through name function and return tree
        if success:
            subtree = ['Parameter1', returned_subtree]
            return [True, returned_index, subtree]
        return [False, token_index, []]

    (success, returned_index, returned_subtree) = Parameter(
        token_index)  # try to run token string through parameter function and return tree

    if success:
        returned_index += 1
        if 'COMMA' == tokens[
            returned_index]:  # check if index is comma and if so increase index
            while tokens[returned_index] == 'COMMA':
                returned_index += 1

                (success, returned_index, returned_subtree) = Parameter(
                    token_index)  # check to see if index matches parameter and if so increase index and check while statement
                subtree.append(returned_subtree)
                returned_index += 1
            return [True, returned_index, subtree]
        subtree = ['ParameterList1', returned_subtree]

        return [True, returned_index, subtree]
    return [False, token_index, []]


def Return(token_index):  # return function
    (success, returned_index, returned_subtree) = Param(
        token_index)  # check index vs parameter to fulfil return requirements
    if success:
        subtree = ["Return0", "RETURN", returned_subtree]
        return [True, returned_index, subtree]  # return subtree
    return [False, token_index, []]


def Functionbody(token_index):  # functionbody check
    # need program function


    bodyfound = 0
    if tokens[
        token_index] != "RETURN":  # check to determine what path to take depending on what token index equals
        bodyfound = 1
        (success, returned_index, returned_subtree) = Program(token_index, 1)
        subtree = ["Program", returned_subtree]
        token_index = returned_index
        temp = []
    if tokens[token_index] == 'RETURN':
        (success, returned_index, returned_subtree) = Return(token_index)
        token_index = returned_index
        if bodyfound == 1:
            subtree.append(returned_subtree)
        else:
            subtree = returned_subtree
        bodyfound = 0
        token_index += 1

        returned_index = token_index
        subtree = ['FunctionBody1', subtree]
        function = 0

        return [True, returned_index, subtree]
    return [False, token_index, []]


def Functionparam(token_index):  # check function param requirements
    if ("RPAREN" == tokens[
        token_index]):  # check to see if token is rparen and if not fail
        subtree = ["FunctonParams1", 'RPAREN']
        returned_index = token_index + 1
        return [True, returned_index, subtree]
    (success, returned_index, returned_subtree) = Namelist(
        token_index)  # call namelist function to get all function variables
    if success:
        subtree = ["FunctonParams1", returned_subtree, 'RPAREN']
        returned_index += 1
        return [True, returned_index, subtree]  # return subtree
    return [False, token_index, []]

    # subtree = ["FunctonParams", returned_subtree]


def FunctionDec(token_index):  # function declare function
    if 'FUNCTION' == tokens[
        token_index]:  # check various conditionals to make sure it matches function format
        token_index += 1
        (success, returned_index, returned_subtree) = Name(token_index)
        if success:
            subtree = returned_subtree
            token_index += 1
            if "LPAREN" == tokens[token_index]:
                token_index += 1
                (success, returned_index, returned_subtree) = Functionparam(
                    token_index)  # call function params to check that syntax
                if success:

                    subtree = subtree, "LPAREN", returned_subtree
                    token_index = returned_index
                    if 'LBRACE' == tokens[token_index]:  # check token indexes
                        token_index += 1
                        (success, returned_index,
                         returned_subtree) = Functionbody(token_index)
                        if success:

                            if "RBRACE" == tokens[returned_index - 2]:
                                returned_subtree = returned_subtree, "RBRACE"
                                subtree = ['FunctionDeclaration0', "FUNCTION",
                                           subtree, 'LBRACE',
                                           returned_subtree]  # setup subtree to return
                                return [True, returned_index - 2, subtree]
    return [False, token_index, []]


def Prints(token_index):  # print function--check for complete syntax
    if ("PRINT" == tokens[token_index]):
        token_index += 1
        (success, returned_index, returned_subtree) = Expression(
            token_index)  # check if object to be printed mathes expression
        if success:
            subtree = ['Print0',
                       'PRINT', returned_subtree]

            return [True, returned_index, subtree]
    return [False, token_index, []]


def Namelist(token_index):  # Namelist Function
    '''
    <NameList> -> <Name> COMMA <NameList> | <Name>
    '''
    (success, returned_index, returned_subtree) = Name(token_index)
    subtree = returned_subtree
    if success:
        token_index += 1
        while tokens[
            token_index] == "COMMA":  # check each name object to make sure it matches syntax
            token_index += 1
            (success, returned_index, returned_subtree) = Name(token_index)
            if success:
                token_index += 1
                subtree = subtree, returned_subtree
            else:
                raise Exception("Namelist Error")
        subtree = ["Namelist0", subtree]
        return [True, returned_index, subtree]  # return subtree

    return [False, token_index, []]


def Assignment(token_index):  # Assignment function
    def SingleAssignment(token_index):
        if 'VAR' == tokens[token_index] and tokens[
                    token_index + 2] == 'ASSIGN' and is_ident(
            tokens[token_index + 1]):  # check assignment syntax
            token_index += 1
            (success, returned_index, returned_subtree) = Name(token_index)
            if tokens[returned_index] == "ASSIGN":
                returned_index += 1
                if success:
                    subtree = returned_subtree
                    (success, returned_index, returned_subtree) = Expression(
                        returned_index)  # Check Expression syntax
                    if success:
                        subtree = ["SingleAssignment0", 'VAR', subtree,
                                   'ASSIGN', returned_subtree]

                        return [True, returned_index, subtree]
        return [False, token_index, []]

    def MultipleAssignment(token_index):  # Multiple assignment checks
        # <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
        if 'VAR' == tokens[token_index]:
            (success, returned_index, returned_subtree) = Namelist(token_index)
            subtree = returned_subtree
            if success and 'ASSIGN' == tokens[returned_index]:
                returned_index += 1
                (success, returned_index, returned_subtree) = FunctionCall(
                    returned_index)
                if success:
                    subtree = ["MultipleAssignment0", subtree,
                               returned_subtree]
                    return [True, returned_index, subtree]
        return [False, token_index, []]

    (success, returned_index, returned_subtree) = SingleAssignment(token_index)
    if success:
        subtree = ["Assignment0", returned_subtree]
        return [True, returned_index, subtree]

    (success, returned_index, returned_subtree) = MultipleAssignment(
        token_index)
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
            (success, returned_index, returned_subtree) = Term(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor> DIV <Term>
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term1", returned_subtree]
        if "DIV" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(
                returned_index + 1)
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
            (success, returned_index, returned_subtree) = Factor(
                returned_index + 1)
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
            (success, returned_index, returned_subtree) = Factor(
                returned_index + 1)
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
            subtree = ["FunctionCall1", returned_subtree]
            if "LPAREN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                (success, returned_index,
                 returned_subtree) = FunctionCallParams(
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
    (success, returned_index, returned_subtree) = Param(token_index)
    if success:
        subtree = ["FunctionCallParams0", returned_subtree]
        if "RPAREN" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            return [True, (returned_index + 1), subtree]
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
        (success, returned_index, returned_subtree) = Expression(
            token_index + 1)
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
    tokens = input()  # get input from user
    tokens = tokens.split(",")
    tokens[len(tokens) - 1] = "EOF"  # add eof to final

    x = Program(0, 0)

    serializedTree = json.dumps(x)  # serialize tree
    print(serializedTree)
