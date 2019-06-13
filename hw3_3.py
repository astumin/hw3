def readNumber(line, index):
    number = 0

    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def ReadMultiply(line, index):
    token = {'type': 'MULTIPLE'}
    return token, index + 1

def ReadDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readLeftParenth(line, index):
    token = {'type': 'LEFTPARENTH'}
    return token, index + 1
    
def readRightParenth(line, index):
    token = {'type': 'RIGHTPARENTH'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '*':
            (token, index) = ReadMultiply(line, index)
        elif line[index] == '/':
            (token, index) = ReadDivide(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '(':
            (token, index) = readLeftParenth(line, index)
        elif line[index] == ')':
            (token, index) = readRightParenth(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def EvaluateMulDiv(tokens):
    answer = 0
    MulDivline=[]
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLE' and tokens[index+1]['type'] == 'NUMBER' and MulDivline != []:
            answer = MulDivline.pop(-1)['number'] * tokens[index+1]['number']
            token = {'type': 'NUMBER', 'number': answer}
            MulDivline.append(token)
            index += 1
        elif tokens[index]['type'] == 'DIVIDE' and tokens[index+1]['type'] == 'NUMBER' and MulDivline != []:
            if tokens[index+1]['number'] == 0:
                print("Can't divide by 0")
                exit(1)
            answer = MulDivline.pop(-1)['number'] / tokens[index+1]['number']
            token = {'type': 'NUMBER', 'number': answer}
            MulDivline.append(token)
            index += 1
        elif tokens[index]['type'] == 'NUMBER' or tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS': 
            MulDivline.append(tokens[index])
        else:
            print('Invalid syntax')
            exit(1)
        index += 1
    return MulDivline


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS' and tokens[index - 2]['type'] == 'NUMBER':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS' and tokens[index - 2]['type'] == 'NUMBER':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def CheckParenth(tokens):
    index = 0
    check = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFTPARENTH':
            check += 1
            index += 1
        elif tokens[index]['type'] == 'RIGHTPARENTH':
            check -= 1
            index += 1
        else:
            index += 1
        if check < 0:
            print('ERROR')
            exit(1)


def CheckInParenth(line):
    if line == []:
        print("ERROR")
        exit(1)


def CountParenth(tokens):
    index = 0
    counter = 0
    CheckParenth(tokens)
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFTPARENTH':
            counter += 1
            index += 1
        else:
            index += 1
    return counter


def ReTokenize(answer, leindex, riindex, tokens):
    retokens = []
    index = 0
    while index < leindex:
        retokens.append(tokens[index])
        index += 1
    retokens.append({'type': 'NUMBER', 'number': answer})
    index = riindex + 1
    while index < len(tokens):
        retokens.append(tokens[index])
        index += 1        
    return retokens


def InParenth(tokens):
    index = 0
    right = 0
    left = 0
    inparatokens = []
    returntokens = []
    #print(tokens)
    while index < len(tokens):
        if tokens[index]['type'] == 'RIGHTPARENTH':
            right = index
            break
        elif tokens[index]['type'] == 'LEFTPARENTH':
            inparatokens=[]
            left = index
        else:
            inparatokens.append(tokens[index])
        index += 1
    CheckInParenth(inparatokens)
    #計算する
    Midanswer = EvaluateMulDiv(inparatokens)
    answer = evaluate(Midanswer)
    returntokens = ReTokenize(answer, left, right, tokens)
    return returntokens


def CulParenth(tokens):
    NumPare = 0
    NumPare =CountParenth(tokens)
    count = 0
    while count < NumPare:
        tokens = InParenth(tokens) 
        count += 1
    return tokens


def Culculation(line):
    Midanswer = CulParenth(line)
    Midanswer = EvaluateMulDiv(Midanswer)
    answer = evaluate(Midanswer)
    return answer


def test(line):
    tokens = tokenize(line)
    actualAnswer = Culculation(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("2*(1+6)")
    test("((3+3)/2+2)")
    print("==== Test finished! ====\n")


runTest()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = Culculation(tokens)
    print(answer)