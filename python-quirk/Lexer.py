import re

final = []
punc = re.compile(r"[+-/*]") # set up regular expressions 
Numbers = re.compile("((\d+(\.\d*)?)|(\.\d+))")
Variables = re.compile("[a-zA-Z]+[a-zA-Z0-9_]*")
Punct = re.compile(r"[,{\}:\".\'\(\)]")
Operaters = re.compile(r"[\+\-\*\/\=\^]")
Keywords = { #Quirk Keywords 
    'print': "PRINT",
    'function': 'FUNCTION',
    'return': 'RETURN',
    'var': 'VAR',
}


def puncfunc(start, point, parse): #Quirk Punc.
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
    while (z == 0):#establish primary loop and declare variables
        matchstart = 0
        pointer = 0
        count = 0
        global final
        final = []
        parse = raw_input()  # get input to parse
        parse = parse.split(" ")
        for i in parse: #set up a loop to go through each index by spaces 
            for letters in i: #go through each character of each index
                if count == 0:
                    word = [parse[pointer]] 
                    word = "".join(word)
                    check = len(word)
                if matchstart == check: #if at index length break
                    break
                if re.search(Punct, parse[pointer][matchstart]): #check to see if any of the indexes matches punc reg ex.
                    puncfunc(matchstart, pointer, parse)
                    matchstart += 1
                elif re.search(Variables, parse[pointer][matchstart]): #check to see if any of the indexes matches variable reg ex
                    checker = 0
                    matchend = matchstart
                    search = matchstart + 1
                    if (re.search(Punct, parse[pointer]) is not None or #check conditionals to see which code to run--Had to do this because index range doesn't include punc so had to check each char and index against reg ex.
                                re.search(Operaters,
                                          parse[pointer]) is not None):
                        while (search - 1 != check and #if match continue until match breaks
                                   re.search(Variables,
                                             parse[pointer][
                                             matchstart:search]) and
                                   (re.search(Variables,
                                              parse[pointer][matchend]) or parse[pointer][matchend] == "_" or
                                            re.search(Numbers,
                                                      parse[pointer][matchend])
                                        is not None)):
                            matchend += 1
                            search += 1
                    else:
                        while (search - 1 != check and re.search(Variables, #check each char against reg ex. #if match continue until match breaks
                                                                 parse[
                                                                     pointer][
                                                                 matchstart:search])):
                            matchend += 1
                            search += 1
                    if parse[pointer][matchstart:matchend] in Keywords:  #check to see if any of the matches characters match a keyword
                        final.insert(len(final),  #insert keyword if match
                                     Keywords.get(parse[pointer]
                                                  [matchstart:matchend]))
                        matchstart = matchend
                        checker = 1
                    if checker == 0: # if no keyword matches run
                        write('variable', matchstart, matchend, word)
                        matchstart = matchend

                elif re.search(Operaters, parse[pointer][matchstart]): #check to see if any of the char match operators
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

                elif re.search(Numbers, parse[pointer][matchstart]): #check to if any of characters match numbers
                    matchend = matchstart
                    while (matchend != check and # if match keep going until the match breaks
                               re.search(Numbers, parse[pointer][matchend])):
                        matchend += 1
                    write('number', matchstart, matchend, word)
                    matchstart = matchend
            pointer += 1
            matchstart = 0

        send = []
        for char in final: #take each index and add comma
            send.append(char + ",")
        x = ''.join(send) #make stiring 
        print(x)
        z += 1


main()
