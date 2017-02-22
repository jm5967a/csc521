import re

punc = re.compile(r"[+-/*]")
Numbers = re.compile("[+-]?((\d+(\.\d*)?)|(\.\d+))")
Variables = re.compile("[a-zA-Z]+[a-zA-Z0-9_]*")
Punct = re.compile(r"[,/[\]:\".\'\(\)]")
Operaters = re.compile(r"[\+\-\*\/\=]")
Keywords = {
    'print': "PRINT ",
    'function': 'FUNCTION ',
    'return': 'RETURN ',
    'var': 'VAR ',
}

final = {}
path = []


class Program(object):
    def __init__(self, line, linecount):
        self.line = line
        self.linecount = linecount

    def inherit(self):
        print("yes")


class Statement(Program):
    def state(self):
        path[0].append(["Statement"])
        flag = 0
        if ("FUNCTION" in self.line[self.linecount]):
            path[0][1].append(["Function Declaration"])
            self.linecount += 1
            parse = self.line[self.linecount]
            print(parse)
            if ("Ident" in parse):
                path[0][1][1].append(["Name"])
                self.linecount += 1
                parse = self.line[self.linecount:self.linecount + 4]
                if (parse[0] == 'LPAREN\n' and parse[1] == 'RPAREN\n'):
                    path[0][1][1][1].append(["Function Params"])
                else:
                    flag = 1
                if (parse[0] == 'LPAREN\n' and parse[3] == "RPAREN\n"):
                    pass
            elif ("Ident" not in parse or flag == 1):
                path[0][1].pop()

            print(path)


# def Expression(line):
#      if(line== "ADD" or line=="SUB"):
#          final.insert(len(final), line)
# def Declaration(count):
#     print(lines[count-1])
# def funcdef(count):
#     print('func\n')
#     print(lines[count - 1])
# def Print():
#    pass
# def Name(value):
#     if("Ident" in value):
#         return True

def main():
    f = open('testfile.txt')
    lines = f.readlines()
    linecount = 0
    path.append(["Program"])
    x = Statement(lines, linecount)
    x.state()


# <Program> -> <Statement> <Program> | <Statement>
#
# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
#
#
# //function declaration statements
# <FunctionDeclaration> -> FUNCTION <Name> <FunctionParams> LBRACE <FunctionBody> RBRACE


main()
