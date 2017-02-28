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
    def Namelist(self):
        self.linecount += 1
        while self.line[self.linecount] != "RPAREN \n":
            if 'Ident' in self.line[self.linecount] or 'NUMBER:' in self.line[self.linecount]:
                x = len(self.line[self.linecount])
                path[0][1][1][1][1].append(self.line[self.linecount][0:x - 1] + " ")
                self.linecount += 1
                if 'RPAREN \n' == self.line[self.linecount]:
                    break
                elif 'COMMA' in self.line[self.linecount]:
                    self.linecount += 1
                else:
                    raise Exception('Invalid Syntax')

            else:
                path[0][1][0].pop()
                raise Exception('Invalid Syntax--Function definition call must end in )')
        return True

    def ParameterList(self):
        pass
    def Functionbody(self):
        self.linecount += 1
        while self.line[self.linecount] != "RETURN \n" and self.linecount + 1 < len(self.line):
            self.linecount += 1
        if (self.line[self.linecount] == "RETURN \n"):
            if self.line[self.linecount] == "RBRACE \n":
                self.linecount += 1
                return
            else:
                pass
        else:
            raise Exception("Function must end in }")
    def Functiondec(self):
        path[0].append(["Statement"])
        flag = 0
        if ("FUNCTION" in self.line[self.linecount]):
            path[0][1].append(["Function Declaration"])
            self.linecount += 1
            parse = self.line[self.linecount]
            print(parse)
            if ("Ident" in parse):
                path[0][1][1].append(["Name: " + parse[:len(parse) - 1]])
                self.linecount += 1
                parse = self.line[self.linecount:self.linecount + 4]
                if (parse[0] == 'LPAREN \n' and parse[1] == 'RPAREN \n'):
                    path[0][1][1][1].append(["Function Params"])
                    self.linecount += 1
                elif (parse[0] == 'LPAREN \n'):
                    path[0][1][1][1].append(["Function Params"])
                    self.Namelist()
            elif ("Ident" not in parse or flag == 1):
                path[0][1].pop()
            self.linecount += 1
            path[0][1][1][1][1].append(["FunctionBody"])
            if self.line[self.linecount] == "LBRACE \n":
                self.Functionbody()


            print(path)


def main():
    f = open('testfile.txt')
    lines = f.readlines()
    linecount = 0
    path.append(["Program"])
    x = Statement(lines, linecount)
    x.Functiondec()


main()
