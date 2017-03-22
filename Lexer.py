import re

final = []
punc = re.compile(r"[+-/*]")
Numbers = re.compile("((\d+(\.\d*)?)|(\.\d+))")
Variables = re.compile("[a-zA-Z]+[a-zA-Z0-9_]*")
Punct = re.compile(r"[,{\}:\".\'\(\)]")
Operaters = re.compile(r"[\+\-\*\/\=\^]")
Keywords = {
    'print': "PRINT",
    'function': 'FUNCTION',
    'return': 'RETURN',
    'var': 'VAR',
}


def puncfunc(start, point, parse):
    Options = {
        '(': "LPAREN",
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ',': 'COMMA',
        ':': 'COLON'
    }
    final.insert(len(final), Options.get(parse[point][start]))


def write(category, start, end, check):
    if category == "variable":
        final.insert(len(final), "IDENT:" + check[start:end])
    elif category == "number":
        final.insert(len(final), "NUMBER:" + check[start:end])


def main():
    z = 0
    while (z == 0):
        matchstart = 0
        pointer = 0
        count = 0
        global final
        final = []
        parse = "function test(v1){var c=3 return c}"
        parse = "var x = (5 * 2) / 5 print x"

        parse = parse.split(" ")
        print(parse)
        for i in parse:
            for letters in i:
                if count == 0:
                    word = [parse[pointer]]
                    word = "".join(word)
                    check = len(word)
                if matchstart == check:
                    break
                if re.search(Punct, parse[pointer][matchstart]):
                    puncfunc(matchstart, pointer, parse)
                    matchstart += 1
                elif re.search(Variables, parse[pointer][matchstart]):
                    checker = 0
                    matchend = matchstart
                    search = matchstart + 1
                    if (re.search(Punct, parse[pointer]) is not None or
                                re.search(Operaters,
                                          parse[pointer]) is not None):
                        while (search - 1 != check and
                                   re.search(Variables,
                                             parse[pointer][
                                             matchstart:search]) and
                                   (re.search(Variables,
                                              parse[pointer][matchend]) or
                                            re.search(Numbers,
                                                      parse[pointer][matchend])
                                        is not None)):
                            matchend += 1
                            search += 1
                    else:
                        while (search - 1 != check and re.search(Variables,
                                                                 parse[
                                                                     pointer][
                                                                 matchstart:search])):
                            matchend += 1
                            search += 1
                    if parse[pointer][matchstart:matchend] in Keywords:
                        final.insert(len(final),
                                     Keywords.get(parse[pointer]
                                                  [matchstart:matchend]))
                        matchstart = matchend
                        checker = 1
                    if checker == 0:
                        write('variable', matchstart, matchend, word)
                        matchstart = matchend

                elif re.search(Operaters, parse[pointer][matchstart]):

                    print(parse[pointer][matchstart])
                    Options = {
                        '+': "ADD",
                        '-': 'SUB',
                        '*': 'MULT',
                        '/': 'DIV',
                        '=': 'ASSIGN',
                        '^': 'EXP'
                    }
                    final.insert(len(final),
                                 Options.get(parse[pointer][matchstart]))
                    matchstart += 1

                elif re.search(Numbers, parse[pointer][matchstart]):
                    matchend = matchstart
                    while (matchend != check and
                               re.search(Numbers, parse[pointer][matchend])):
                        matchend += 1
                    write('number', matchstart, matchend, word)
                    matchstart = matchend
            pointer += 1
            matchstart = 0
        file = open('testfile.txt', 'w')
        for char in final:
            file.write(char + ",")
        file.close()
        print(final)
        z += 1


main()
