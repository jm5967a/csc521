from __future__ import print_function

import json
import pprint
import sys

pp = pprint.PrettyPrinter(indent=1, depth=100)  # ident 1 each time,
# max depth of 100

tree = ['Value0', ['Name1', 'SUB', 'IDENT:x']]
tree = ['FunctionDeclaration0',
        'FUNCTIION',
        ['Name0', 'IDENT:FooFunk'],
        'LPAREN',
        ['FunctionParams0',
         ['NameList0',
          ['Name0', "IDENT:a"],
          'COMMA',
          ['NameList1', ['Name0', "IDENT:b"]]],
         'RPAREN'],
        'LBRACE',
        ['FunctionBody1',
         ['Return0',
          ['NameList0',
           ['Name0', "IDENT:y"],
           'COMMA',
           ['NameList1', ['Name0', "IDENT:z"]]]

          ]],
        'RBRACE']

'''Scope example:
var x = 4 #{'x':4}
function foo(z) {
    foo(z/2)
    return z + x
}
foo(14)
Inside of foo(14), the scope looks like this:
{
 'z':7,
 "__parent__": {
    'z':14,
    "__parent__": {
        'x':4
    }
 }
}
'''

'''For testing function calls. The source:
FooFunk(x - 4, z)
'''
tree_with_function_call = ["FunctionCall0",
                           ['Name0', "IDENT:FooFunk"],
                           'LPAREN',
                           ['FunctionCallParams0',
                            ["ParameterList0",
                             ["Parameter0",
                              ['Expression1',
                               ['Term2',
                                ['Factor4', ['Value0', ['Name0', 'IDENT:x']]]],
                               'SUB',
                               ['Expression2',
                                ['Term2', ['Factor4', ['Value1', ['Number0',
                                                                  'NUMBER:4']]]
                                 ]
                                ]
                               ]
                              ],
                             'COMMA',
                             ['ParameterList1',
                              ['Parameter1', ['Name0', "IDENT:z"]]
                              ]
                             ],
                            'RPAREN'
                            ]
                           ]

scope_with_function = {
    'x': 100,
    'z': 101,
    'FooFunk': [['a', 'b'],
                ['FunctionBody1',
                 ['Return0',
                  ['NameList0',
                   ['Name0', 'IDENT:y'],
                   'COMMA',
                   ['NameList1', ['Name0', 'IDENT:z']]]]]]}


# start utilities
def eprint(msg):
    '''Prints to stderr.
    '''
    print(msg, file=sys.stderr)


def lookup_in_scope_stack(name, scope):
    '''Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    '''
    # turn this on for better debugging
    # eprint("lookup_in_scope_stack() "+ str(name))

    if name in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            eprint("not found in scope. Looking at __parent__")
            return lookup_in_scope_stack(name, scope["__parent__"])


def get_name_from_ident(tok):  # gets the variable name
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    eprint("get_name_from_ident() " + tok)
    colon_index = tok.find(":")
    return tok[colon_index + 1:]


def get_number_from_ident(tok):  # gets the number
    '''Returns the float lexeme associated with an NUMBER token, tok.
    '''
    eprint("get_number_from_ident() " + tok)
    colon_index = tok.find(":")
    return float(tok[colon_index + 1:])


def func_by_name(*args):
    '''Calls a function whos name is given as a parameter. It requires the
    parse tree associated with that point in the grammar traversal and the
        current scope.
    *args is interpreted as
        name = args[0] -- the name of the function to call
        pt = args[1] -- the subtree of the parse tree associated with the name
        scope = args[2] -- the scope the subtree should use
    return - Pass through the return value of the called function.
    '''
    name = args[0]
    pt = args[1]
    scope = args[2]

    returnval = globals()[name](pt, scope)
    eprint("calfunc_by_name()) " + name + " " + str(returnval))
    return returnval


# end utilities

# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)
    func_by_name(pt[2][0], pt[2], scope)


def Program1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Statement1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Statement2(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def FunctionDeclaration0(pt, scope):  # gets the function
    '''
    1. Get function name.
    2. Get names of parameters.
    3. Get reference to function body subtree.
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }
    #Bonus: check for return value length at declaration time
    '''
    fname = func_by_name(pt[2][0], pt[2], scope)[1]
    pnames = func_by_name(pt[4][0], pt[4], scope)
    scope[fname] = [pnames, pt[6]]


# <FunctionParams> -> <NameList> RPAREN | RPAREN
# should return a list of values
def FunctionParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionParams1(pt, scope):
    return []


# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    return func_by_name(pt[2][0], pt[2], scope)


# <Assignment> -> <SingleAssignment> | <MultipleAssignment>

# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Assignment1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    # 1. Get name of the variable.
    # 2. Get value of <Expression>
    # 3. Bind name to value in scope.
    # Bonus: error if the name already exists in scope -- no rebinding
    vname = func_by_name(pt[2][0], pt[2], scope)[1]
    value = func_by_name(pt[4][0], pt[4], scope)
    scope[vname] = value


# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):  # gets all of the variables and the values
    # 1. Get list of variable names
    # 2. Get the values returned from the fuction call
    # Bonus: error if any name already exists in scope -- no rebinding
    # Bonus: error if the number of variable names does not match the number
    # of values
    func_by_name(pt[2][0], pt[2], scope)
    func_by_name(pt[4][0], pt[4], scope)


# <Print> -> PRINT <Expression>    #print function
def Print0(pt, scope):
    print(str(func_by_name(pt[2][0], pt[2], scope)))


# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)


def NameList1(pt, scope):
    # getting the [1] of the return value for name as it returns a [val, name]
    return [func_by_name(pt[1][0], pt[1], scope)[1]]


# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
# should return a a list of values.
def ParameterList0(pt, scope):
    val = func_by_name(pt[1][0], pt[1], scope)
    return [val] + func_by_name(pt[3][0], pt[3], scope)


def ParameterList1(pt, scope):
    return [func_by_name(pt[1][0], pt[1], scope)]


# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def Parameter1(pt, scope):
    # pull value out of [value,name]
    return func_by_name(pt[1][0], pt[1], scope)[0]


def Expression0(pt, scope):
    # <Term> ADD <Expression>
    val1 = func_by_name(pt[1][0], pt[1], scope)
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 + val2


def Expression1(pt, scope):
    # <Term> SUB <Expression>
    val1 = func_by_name(pt[1][0], pt[1], scope)
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 - val2


def Expression2(pt, scope):
    # <Term>
    return func_by_name(pt[1][0], pt[1], scope)


# <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    # <Factor>
    val1 = func_by_name(pt[1][0], pt[1], scope)
    # MULT
    # <Term>
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 * val2


def Term1(pt, scope):
    # <Factor>
    val1 = func_by_name(pt[1][0], pt[1], scope)
    # DIV
    # <Term>
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 / val2


def Term2(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope, scope)


# <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall>
# | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    val1 = func_by_name(pt[1][0], pt[1], scope)
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 ** val2


def Factor1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def Factor2(pt, scope):
    # returns multiple values -- use the first by default.
    return func_by_name(pt[1][0], pt[1], scope)


def Factor3(pt, scope):
    val1 = func_by_name(pt[1][0], pt[1], scope)
    val2 = func_by_name(pt[3][0], pt[3], scope)
    return val1 ** val2


def Factor4(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number>
# | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):  # gets the function name, makes new scope,
    # gets parameter values, runs the function body subtree
    '''
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.
    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored
     function information.
    7. Get the index return number.
    8. Return one value from the list of return values that corresponds
    to the index number.
    Bonus: Flag an error if the index value is greater than the number of
    values returned by the function body.
    '''
    functionscop = {"parent:": scope}  # new scope
    value = func_by_name(pt[1][0], pt[1], scope)
    function_store = value[0]
    findex = int(func_by_name(pt[5][0], pt[5], scope))
    pvalues = func_by_name(pt[3][0], pt[3], scope)  # pget aram values
    pnames = function_store[0]  # get param names
    for index in range(0, len(pvalues)):
        functionscop[pnames[index]] = pvalues[index]
    returns = func_by_name(function_store[1][0], function_store[1],
                           functionscop)
    return returns[findex]


def FunctionCall1(pt, scope):
    '''
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.
    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored function
    information.
    7. Return the list of values generated by the <FunctionBody>
    '''
    functionscop = {"parent:": scope}  # new scope
    value = func_by_name(pt[1][0], pt[1], scope)
    function_store = value[0]
    pvalues = func_by_name(pt[3][0], pt[3], scope)  # get param values
    pnames = function_store[0]  # get param names
    for index in range(0, len(pvalues)):
        functionscop[pnames[index]] = pvalues[index]
    returns = func_by_name(function_store[1][0], function_store[1],
                           functionscop)  # setup call to func_byname utility
    # to get return
    return returns


# <FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionCallParams1(pt, scope):
    return []


# <SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    return func_by_name(pt[2][0], pt[2], scope)


# <Value> -> <Name> | <Number>
def Value0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)[0]


def Value1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    name = get_name_from_ident(pt[1])
    return [lookup_in_scope_stack(name, scope), name]


def Name1(pt, scope):
    name = get_name_from_ident(pt[2])
    return [-lookup_in_scope_stack(name, scope), name]


def Name2(pt, scope):
    name = get_name_from_ident(pt[2])
    return [lookup_in_scope_stack(name, scope), name]


# <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    return get_number_from_ident(pt[1])


def Number1(pt, scope):
    return -get_number_from_ident(pt[2])


def Number2(pt, scope):
    return get_number_from_ident(pt[2])


# corresponds to: print 1 + 4 - 3
e1tree = ['Program1',
          ['Statement2',
           ['Print0',
            'PRINT',
            ['Expression0',
             ['Term2', ['Factor4', ['Value1', ['Number0', 'NUMBER:1']]]],
             'ADD',
             ['Expression1',
              ['Term2', ['Factor4', ['Value1', ['Number0', 'NUMBER:4']]]],
              'SUB',
              ['Expression2',
               ['Term2',
                ['Factor4', ['Value1', ['Number0', 'NUMBER:3']]]]]]]]]]

e1tree = raw_input()  # get user input

try:
    e1tree = json.loads(e1tree)  # deserialize input
except:

    list(e1tree)

if __name__ == '__main__':
    # choose a parse tree and initial scope
    tree = e1tree
    scope = {}  # establish scope
    # execute the program starting at the top of the tree
    func_by_name(tree[0], tree, scope)  # call main function
    # Uncomment to see the final scope after the program has executed.
# pp.pprint(scope)
