#! /usr/bin/python3
# if functions are too big for lexer/parser files, add them here and import accordingly
desc = {
  'LIST' : 'Creates an array containing identifiers',
  'AND' : 'Conditional statement',
  'ASSIGN' :'Assigns a value to multiple identifier',
  'NEGATIVE' : 'Turns value of identifier into a negative one',
  'ASK' : 'Asks user for a value input for an identifier',
  'BREAK' : 'Breaks current operation in line of code',
  'CALLING' : 'Calls a function',
  'CHAR' : 'Char value',
  'CONTAINING' : 'Shows content of list',
  'DIVIDE' : 'Used to perform the mathematical operation of division',
  'FIGURATIVELY' : 'Allows for substitution of numerals into actual number values',
  'FIN' : 'Indicates the end of a function.',
  'RETURN' : 'Returns value of identifier called',
  'FROM' : 'From the location',
  'CONTINUE' : 'Allows process to continue if condition asked for is satisfied',
  'IF' : 'Characters i, f Starts a block statement',
  'INTO' : 'Into the location',
  'EQ' : '==',
  'NEQ' : '!=',
  'ITEM' : 'Value in a list',
  'LENGTH' : 'Takes length of an identifier',
  'MINUS' : 'Used to perform the mathematical operation of subtraction',
  'MODULO' : 'Used to perform the mathematical operation of modulo',
  'NOT' : 'The negation unary operator',
  'PROGSTART' : 'Indicates the start of the main program',
  'OF' : 'Used in conjunction with an operator',
  'OR' : 'conditional statement',
  'ELSE' : 'Used within if statements',
  'PLUS' : 'Used to perform the mathematical operation of addition',
  'PUSH' : 'Pushes a value into a stack',
  'POP' : 'Pops the top value of a stack',
  'EXP' : 'Used to perform the mathematical operation of exponation',
  'REMOVE' : 'Removes the nth item from the list',
  'SAY' : 'Prints out the statement input',
  'PROGEND' : 'Ends the main program',
  'TIMES' : 'Used to perform the mathematical operation of multiplication',
  'ELIF' : 'Used in continuation with if statements',
  'WHILE' : 'Used to initiate while loops',
  'WITH' : 'Used in calling a function or returning a statement or value',
  'ID' : 'Any string starting with a letter, followed by more letters or underscores',
  'SNUM' : 'Number literature',
  'FIGNUM' : 'Number literature',
  'STRING' : 'String literature',
  'TRUE' : 'Assigns a condition to an identifier',
  'FALSE' : 'Assigns a condition to an identifier',
  'NOTHING' : 'Assigns a null value ',
  'EMPTY' : 'Assigns a null value ',
  'DOT' : 'Terminating symbol for lines',
  'COLON' : 'Connotes values in scope of certain functions',
  'COMMA' : 'Used to grammarly correct code',
  'GT' : '>',
  'LT' : '<',
  'GTE' : '>=',
  'LTE' : '<=',
  'L_PAR' : '(',
  'R_PAR' : ')'
}


predict_set_dict = {
    'PROGSTART': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not', 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list'],
    'AND': ['true', 'false', 'id', 'nothing', 'item', 'pop', 'snum', 'pnum', 'char', 'length', 'stringterm', 'String_wsub', 'calling', 'a list'],
    'ASK': ['id', 'stringterm', 'String_wsub', 'item'],
    'ASSIGN': ['stringterm', 'String_wsub', 'id', 'true', 'false', 'nothing', 'char', 'calling', 'pop', 'item', 'a list'],
    'CHAR': ['id', 'snum', 'stringterm', 'String_wsub'],
    'COLON': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not' 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list'],
    'COMMA': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'DIVIDE': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'DOT': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not' 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list'],
    'ELIF': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'ELSE': [':'],
    'EQ': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'EXP':  ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'FALSE': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really"],  # this
    'FIGNUM': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really", 'of'],  # this
    'FIN': ['.'],
    'FROM': ['id', 'INTO'],
    'GT' : ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'GTE' : ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'ID' : ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really", 'is', 'are'],  # this
    'IF':  ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'INTO': ['id'],
    'ITEM': ['snum'],
    'LENGTH': ['stringterm', 'id', 'a list'],
    'LT': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'LTE': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'L_PAR': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'MINUS': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'MODULO': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'NEQ': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'NOT': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'NOTHING': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really"],  # this
    'OF': ['id', 'stringterm'],
    'OR': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'PLUS': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'POP': ['FROM'],
    'PUSH':  ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'R_PAR': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really"],  # this
    'RETURN': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'SAY':  ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'BREAK': ['.'],
    'CONTINUE': ['.'],
    'CONTAINING': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'LIST': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really", 'containing'],  # this
    'SNUM':  ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really", 'of'],  # this
    'stringterm':  ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really"],  # this
    'TIMES':  ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'TO':  ['id'],
    'TRUE': ['.', ',', ':', '+', '-', '*', '/', '%', '^', '>', '<', '>=', '<=', '==', '!=', 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', 'to the power of', 'is greater than', 'is less than', 'is equal to', 'is really', 'is not equal to', "isn't really"],  # this
    'WHILE': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'REMOVE': ['item'],
    'CALLING': ['id'],
    'WITH': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
}

def poetic_to_specific(numbers):
    """
    Converts words to numbers.
    epic = 4
    tea, i what = 3.14
    how, how how how, = 4.334
    """
    decimal = ""
    fractional = ""
    num_equiv = 0
    numstr_equiv = ""
    if "," in numbers:
        decimal = numbers.split(",", maxsplit=1)[0]
        fractional = numbers.split(",", maxsplit=1)[1]
        decimal = decimal.split(' ')
        fractional = fractional.split(' ')
        while fractional:
            if fractional[0] == '':
                fractional.remove(fractional[0])
                continue
            result = len(fractional[0])
            if result >= 10: result %= 10
            numstr_equiv += str(result)
            fractional.remove(fractional[0])
        fractional_length = len(numstr_equiv)
        num_equiv = int(numstr_equiv) * 10 ** -fractional_length
    else: decimal = numbers.split(' ')
    while decimal:
        if decimal[0] == '':
            decimal.remove(decimal[0])
            continue
        result = len(decimal[0])
        if result >= 10: result %= 10
        num_equiv += result * (10 ** (len(decimal)-1))
        decimal.remove(decimal[0])
    return num_equiv
