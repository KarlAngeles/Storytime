#! /usr/bin/env python3
import ply.lex as lex
import re
from helpers import poetic_to_specific

class StorytimeLexingError(Exception):
    def __init__(self, message):
        self.message = message

reserved = {
    'and': 'AND',
    'are': 'ASSIGN',
    'ask': 'ASK',
    'containing': 'CONTAINING',
    'calling': 'CALLING',
    'char': 'CHAR',
    'with': 'WITH',
    'break': 'BREAK',
    'stop': 'BREAK',
    'go': 'CONTINUE',
    'empty': 'NOTHING',
    'false': 'FALSE',
    'if': 'IF',
    'into': 'INTO',
    'is': 'ASSIGN',
    'item': 'ITEM',
    'minus': 'MINUS',
    'modulo': 'MODULO',
    'not': 'NOT',
    'nothing': 'NOTHING',
    'of': 'OF',
    'or': 'OR',
    'plus': 'PLUS',
    'pop': 'POP',
    'push': 'PUSH',
    'raised to': 'EXP',
    'say': 'SAY',
    'times': 'TIMES',
    'to': 'TO',
    'true': 'TRUE',
    'unless': 'ELIF',
    'otherwise': 'ELSE',
    'while': 'WHILE',
    'remove': 'REMOVE',
    'from': 'FROM',
    'fin': 'FIN',
    'figuratively': 'FIGURATIVELY',
    'arrogant': 'NEGATIVE',
    'biased': 'NEGATIVE',
    'hateful': 'NEGATIVE',
    'negative': 'NEGATIVE',
    'plebian': 'NEGATIVE',
    'selfish': 'NEGATIVE',
    'tasteless': 'NEGATIVE',
    'toxic': 'NEGATIVE',
    'trashy': 'NEGATIVE',
}

tokens = (
    'PROGSTART',
    'AND',
    'ASK',
    'ASSIGN',
    'COLON',
    'CHAR',
    'COMMA',
    'DIVIDE',
    'DOT',
    'ELIF',
    'ELSE',
    'EQ',
    'EXP',
    'FALSE',
    'FIGNUM',
    'FIN',
    'FROM',
    'GT',
    'GTE',
    'ID',
    'IF',
    'INTO',
    'ITEM',
    'LENGTH',
    'LT',
    'LTE',
    'L_PAR',
    'MINUS',
    'MODULO',
    'NEQ',
    'NOT',
    'NEGATIVE',
    'NEWLINE',
    'NOTHING',
    'OF',
    'OR',
    'PLUS',
    'POP',
    'PUSH',
    'R_PAR',
    'RETURN',
    'SAY',
    'BREAK',
    'CONTINUE',
    'CONTAINING',
    'LIST',
    'SNUM',
    'STRING',
    'STRING_SUB',
    'TIMES',
    'TO',
    'TRUE',
    'WHILE',
    'REMOVE',
    'CALLING',
    'WITH',
    'FIGURATIVELY',
    'PROGEND',
)

t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'\.'

t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
# t_EQ = r'=='
# t_NEQ = r'!='

t_L_PAR = r'\('
t_R_PAR = r'\)'

t_PLUS = r'\+'
# t_MINUS = r'-'
t_TIMES = r'\*'
# t_DIVIDE = r'/'
t_MODULO = r'%'
# t_EXP = r'\^'

t_ignore = ' \t\n'

div = r'(divided\ by' + r'|' + r'/)'
eq = r'(is\ equal\ to' + r'|' + r'is\ really' + r'|' + r'==)'
exp = r'(to\ the\ power\ of' + r'|' + r'raised\ to' + r'|' + r'\^)'
minus = r'(\-' + r'|' + r'negative\ of)'
neq = r'(isn\'t\ equal\ to' + r'|' + r'is\ not\ equal\ to' + r'|' + r'isn\'t\ really' + r'|' + r'!=)'
# gt = r'(greater\ than' + r'|' + r'>)'
# lt = r'(less\ than' + r'|' + r'<)'
# gte = r'(greater\ than\ or\ equal\ to' + r'|' + r'>=)'
# lte = r'(less\ than\ or\ equal\ to' + r'|' + r'<=)'

id = r'[a-zA-Z]([a-zA-Z\_]*)?'
s_num = r'\d\.(\d+)' + r'|' + r'\d+'
fig_num = r'figuratively\ ' + r'([a-zA-Z\,]([a-zA-Z\ \,]*)?)+'
string = r'\".*\s*\"'

p_end = r'The\ end.'
p_start = 'Once\ upon\ a\ time,'

ret = r'finish\ with'
list_token = r'a\ list'
length = 'length\ of'

@lex.TOKEN(p_start)
def t_PROGSTART(t):
    return t

@lex.TOKEN(p_end)
def t_PROGEND(t):
    return t

@lex.TOKEN(ret)
def t_RETURN(t):
    return t

@lex.TOKEN(exp)
def t_EXP(t):
    return t

@lex.TOKEN(minus)
def t_MINUS(t):
    return t

@lex.TOKEN(div)
def t_DIVIDE(t):
    return t

@lex.TOKEN(eq)
def t_EQ(t):
    return t

@lex.TOKEN(neq)
def t_NEQ(t):
    return t

# @lex.TOKEN(gt)
# def t_GT(t):
    # return t
# @lex.TOKEN(lt)
# def t_LT(t):
    # return t

# @lex.TOKEN(gte)
# def t_GTE(t):
    # return t

# @lex.TOKEN(lte)
# def t_LTE(t):
    # return t

@lex.TOKEN(fig_num)
def t_FIGNUM(t):
    t.value = poetic_to_specific(t.value[13:])
    # need to fix this
    # if t.value in reserved:
        # raise StorytimeLexingError("Lexical Error: Poetic numbers cannot contain reserved words")
    return t

@lex.TOKEN(s_num)
def t_SNUM(t):
    if (type(t.value) == float):
        t.value = float(t.value)
    elif (type(t.value) == int):
        t.value = int(t.value)

    return t

@lex.TOKEN(list_token)
def t_LIST(t):
    return t

@lex.TOKEN(length)
def t_LENGTH(t):
    return t

@lex.TOKEN(id)
def t_ID(t):
    if t.value in reserved:
        t.type = reserved[t.value]
    if len(t.value) > 45:
        raise StorytimeLexingError("Lexical Error: Exceeds limit for identifier: {} at {} {}".format(t.value, t.lexer.lineno, t.lexer.lexpos))
    return t

@lex.TOKEN(string)
def t_STRING(t):
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def errors_func():
    return errors

def t_error(t):
    # if (not previousToken):
        # previousTok  en = t.value
    # previousToken = 'Once upon a time,'
    # print(t.value)

    raise StorytimeLexingError("Lexical Error: Unexpected character: {} at {} {}".format(t.value[0], t.lexer.lineno, t.lexer.lexpos))
    # print("Lexical Error: Unexpected character: {} at ({} {})".format(t.value[0], t.lexer.lineno, t.lexer.lexpos))
    # if (delimDict[previousToken] == t.value):
        # raise StorytimeLexingError("Lexical error: Invalid delimiter")

    # print(delimDict['Once upon a time,']) 
    # print(t.value)

def t_eof(t):
    return None

# invalid
whitespace = []
delim4 = ['"', '+', '-', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', '(', ')']
delim5 = ['.', ',', ':', '+', '-', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', '(', ')']
delim6 = ['.', ',', ':', '+', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', ')']
delim7 = [',',  ':', '"', '+', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', '(', ')', 'NUMBERS']
delim8 = ['.', ',', ':', '"', ')', '+', '*', '/', '^', '%', '<', '>', '<=', '>=', '==', '!=']
delim9 = ['.', ',', ':', '+', '-', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', ')', 'NUMBERS']
delim10 = ['.', ',', '"', '+', '-', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', '(', ')', 'NUMBERS']
delim11 = ['.', ',', ':', '+', '*', '/', '^', '%', '>', '<', '<=', '>=', '==', '!=', ')']
delim12 = ['"', '(']
delim_id = ['"', '(', 'NUMBERS']
revised_delim_id = ['"', 'NUMBERS']

delimDict = {
    # keywords
    'a list': delim_id,
    'and': delim6,
    'are': delim6,
    'arrogant': delim4,
    'ask': delim5,
    'biased': delim4,
    'break': delim7,
    # ‘calling’:
    'char': delim8,
    'containing': delim6,
    'divided by': delim6,
    'empty': delim_id,
    'false': delim_id,
    'fin': delim7,
    'finish with': delim6,
    # 'from': 
    'go': delim7,
    'hateful': delim4,
    'if': delim6,
    # 'into': 
    'is': delim6,
    'is equal to': delim6,
    "isn' equal to": delim6,
    'is not equal to': delim6,
    'is really': delim6,
    "isn't really": delim6,
    'item': delim8,
    'length of': delim9,
    'minus': delim6,
    'modulo': delim6,
    'negative': delim4,
    'negative of': delim6,
    'not': delim6,
    'nothing': delim_id,
    # 'of': 
    'or': delim6,
    'otherwise': delim10,
    'plebeian': delim4,
    'plus': delim6,
    'push': delim6,
    # 'pop': 
    'raised to': delim6,
    # 'remove': 
    'say': delim6,
    'selfish': delim4,
    'stop': delim7,
    'tasteless': delim4,
    'times': delim6,
    'to the power of': delim6,
    'toxic': delim4,
    'trashy': delim4,
    'true': delim_id,
    'unless': delim6,
    'while': delim6,
    'with': delim6,
    'SNUM': delim12,
    'STRING': delim12,
    'ID': revised_delim_id,
    # symbols
    '.': delim11,
    ':': delim11,
    ',': delim11,
    '+': delim11,
    '-': delim11,
    '*': delim11,
    '/': delim11,
    '%': delim11,
    '^': delim11,
    '==': delim11,
    '!=': delim11,
    '>': delim11,
    '<': delim11,
    '>=': delim11,
    '<=': delim11,
    '(': delim11,
    ')': delim12,
}

toks = []
errors = []
previousToken = ''

lexer = lex.lex()

def get_errors():
    return errors

# data = '''
# to
# '''

# # need to throw error when multiple symbols
# lexer.input(data)
# while true:
    # tok = lexer.token()
    # if not tok:
        # break

    # try:
        # # list of invalid 

        # # accounts for type tokens (id, snum, string) and checks if current token is valid accrdg to prev token
        # if (previoustoken.type in ['snum', 'string', 'id']):
            # typeval = delimdict[previoustoken.type]
            # if (tok.value in typeval or (tok.type == 'snum' and 'numbers' in typeval)):
                # toks.pop()
                # raise storytimelexingerror('lexical error: invalid delimiter for "{}" token: [{} {} {} {}]'.format(previoustoken, tok.type, tok.value, tok.lineno, tok.lexpos))

        # # checks if current token is valid or invalid 
        # elif (tok.value in delimdict[previoustoken.value] or (tok.type == 'snum' and 'numbers' in delimdict[previoustoken.value])):
            # toks.pop()
            # raise storytimelexingerror('lexical error: invalid delimiter for "{}" token: [{} {} {} {}]'.format(previoustoken, tok.type, tok.value, tok.lineno, tok.lexpos))

        # # whatever token is read it's added to toks list
        # previoustoken = tok
        # toks.append(tok)
    # except:
        # previoustoken = tok
        # toks.append(tok)

# if (errors):
    # for error in errors:
        # print(error)
# else:
    # for token in toks:
        # print(token)
