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

def readMultiply(line, index):
    token = {'type': 'MULTIPLE'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluateMulDiv(tokens):
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


def test(line):
    tokens = tokenize(line)
    MidExp = evaluateMulDiv(tokens)
    actualAnswer = evaluate(MidExp)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2")
    test("1-2")
    test("1.1+2")
    test("1.0-3.02")

    test("2*3")
    test("8/2")
    test("4*2+1")
    test("4+2/3")
    test("5.1*4-1")
    test("1.63+4/3")
    test("3*3/0")

    #test("1+-2")
    #test("+-1+1")
    #test("3/0")
    #test("4**4")
    #test("*3+4")

    print("==== Test finished! ====\n")

runTest()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    MidExp = evaluateMulDiv(tokens)
    answer = evaluate(MidExp)
    print("answer = %f\n" % answer)