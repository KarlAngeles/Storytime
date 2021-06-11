import lexer
import ply.yacc as yacc

last_token = None
second_last_token = None
tokens = lexer.tokens

class StorytimeParsingError(Exception):
    def __init__(self, message):
        self.message = message

precendence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'GT', 'LT', 'EQ', 'NEQ', 'GTE', 'LTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),
    ('left', 'EXP'),
    ('left', 'L_PAR', 'R_PAR'),
)

predict_set_dict = {
    'PROGSTART': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not', 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list'],
    'AND': ['true', 'false', 'id', 'nothing', 'item', 'pop', 'snum', 'pnum', 'char', 'length', 'stringterm', 'String_wsub', 'calling', 'a list'],
    'ASK': ['id', 'stringterm', 'String_wsub', 'item'],
    'ASSIGN': ['stringterm', 'String_wsub', 'id', 'true', 'false', 'nothing', 'char', 'calling', 'pop', 'item', 'a list'],
    'CHAR': ['id', 'snum', 'stringterm', 'String_wsub'],
    'COLON': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not' 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list'],
    'COMMA': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'DIVIDE': ['(', '-', 'not', 'id', 'stringterm', 'nothing', 'true', 'false', 'calling', 'snum', 'pnum', 'a list', 'item', 'pop', 'char', 'length'],
    'DOT': ['stringterm', 'String_wsub', 'id', 'nothing', 'true', 'false', 'item', 'not', 'pop', 'push', 'continue', 'break', 'if', 'unless', 'otherwise', 'snum', 'pnum', 'length', '(', 'say', 'ask', 'char', 'remove', 'calling', 'while', 'a list', 'fin'],
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
    'PROGEND': ['EOF'],
}

def p_program(p):
    '''program : function_declarations PROGSTART statements PROGEND
               | PROGSTART statements PROGEND
    '''
    pass

def p_program_error(p):
    '''program : function_declarations statements PROGEND
               | function_declarations PROGSTART statements
               | PROGSTART statements
               | statements PROGEND
               | PROGSTART
               | TO
               | statements
               | expression
    '''
    print(p)
    if p[1] == 'to':
        try:
            if p[2] != 'Once upon a time,':
                raise StorytimeParsingError('Missing program start')
            elif p[3] != 'The end.':
                raise StorytimeParsingError('Missing program end')
        except:
            raise StorytimeParsingError('Missing main function')
    elif len(p) == 2 and p[1] == 'Once upon a time,':
        raise StorytimeParsingError('Missing program end')
    else:
        if p[1] != 'Once upon a time,':
            raise StorytimeParsingError('Missing program start')
        elif p[2] != 'The end.':
            raise StorytimeParsingError('Missing program end')

def p_function_declarations(p):
    '''function_declarations : function_declarations function_declaration
                             | function_declaration
    '''
    pass

def p_function_declaration(p):
    '''function_declaration : TO ID declaration_parameter COLON statements FIN DOT
                            | TO ID COLON statements FIN DOT
    '''
    pass

def p_declaration_parameter(p):
    '''declaration_parameter : L_PAR declaration_parameter_value R_PAR
    '''
    pass

def p_declaration_parameter_value(p):
    '''declaration_parameter_value : ID COMMA declaration_parameter_value
                                   | ID
    '''
    pass

def p_statements(p):
    '''statements : statements statement
                  | statement
    '''
    pass

def p_statement(p):
    '''statement : dot_statement
                 | block_statement
    '''
    pass

# moved some to valid_values
def p_dot_statement(p):
    '''dot_statement : expression DOT
                     | return_statement DOT
                     | function_call DOT
                     | say_statement DOT
                     | ask_statement DOT
                     | assignment_statement DOT
                     | list_remove DOT
                     | list_push DOT
                     | list_pop_assssignment DOT
                     | CONTINUE DOT
                     | BREAK DOT
    '''
    pass

def p_block_statement(p):
    '''block_statement : if_statement
                       | while_statement
    '''
    pass

def p_if_statement(p):
    '''if_statement : IF expression COLON statements FIN DOT elif_statements
                    | IF expression COLON statements FIN DOT else_statement
                    | IF expression COLON statements FIN DOT
    '''
    pass


def p_elif_statements(p):
    '''elif_statements : elif_statements elif_statement
                       | elif_statements else_statement
                       | elif_statement
    '''
    pass

def p_elif_statement(p):
    '''elif_statement : ELIF expression COLON statements FIN DOT
    '''
    pass

def p_else_statement(p):
    '''else_statement : ELSE COLON statements FIN DOT
    '''
    pass

def p_while_statement(p):
    '''while_statement : WHILE expression COLON statements FIN DOT
    '''
    pass


# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
# expression not included
def p_valid_values(p):
    '''valid_values : function_call
                    | ID
                    | STRING
                    | num
                    | NOTHING
                    | boolean
                    | list_assignment
                    | list_access
                    | list_pop
                    | string_access
                    | length_of
    '''
    pass

# multiple assignment not supported anymore
# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
def p_assignment_statement(p):
    '''assignment_statement : assignment_statement_variables ASSIGN expression
    '''
    pass

def p_assignment_statement_variables(p):
    '''assignment_statement_variables : ID COMMA assignment_statement_variables
                                      | ID
                                      | list_access COMMA assignment_statement_variables
                                      | list_access
    '''
    pass

def p_function_call(p):
    '''function_call : CALLING ID
                     | CALLING ID WITH list_assignment_value
    '''
    pass

# now supports multiple values 
# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
def p_say_statement(p):
    '''say_statement : SAY list_assignment_value
    '''
    pass


def p_ask_statement(p):
    '''ask_statement : ASK STRING
                     | ASK ID STRING
                     | ASK list_access STRING
    '''
    pass

# this is wrong need to fix next time
# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
def p_return_statement(p):
    '''return_statement : RETURN valid_values
    '''
    pass


def p_string_access(p):
    '''string_access : CHAR num OF ID
                     | CHAR num OF STRING
    '''
    pass

def p_length_of(p):
    '''length_of : LENGTH STRING
                 | LENGTH ID
                 | LENGTH list_assignment
    '''

def p_list_assignment(p):
    '''list_assignment : LIST
                       | LIST CONTAINING list_assignment_value
    '''
    pass

# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
# need to add expression here
def p_list_assignment_value(p):
    '''list_assignment_value : list_assignment_value COMMA list_assignment_value
                             | expression
    '''
    pass

def p_list_remove(p):
    '''list_remove : REMOVE list_access
    '''
    pass


def p_list_access(p):
    '''list_access : ITEM num OF ID
    '''
    pass


# now supports multiple values
def p_list_push(p):
    '''list_push : PUSH list_assignment_value INTO ID
    '''
    pass


def p_list_pop(p):
    '''list_pop : POP FROM ID
    '''
    pass


def p_list_pop_assignment(p):
    '''list_pop_assssignment : POP FROM ID INTO ID
    '''
    pass


# valid values: function call, id, string, num, nothing, boolean, list_assignment, list_access, list_pop
def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EXP expression
                  | L_PAR expression R_PAR
                  | MINUS expression
                  | expression GT expression
                  | expression LT expression
                  | expression GTE expression
                  | expression LTE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression OR expression
                  | expression AND expression
                  | NOT expression
                  | valid_values
    '''
    pass

def p_num(p):
    '''num : SNUM
           | FIGNUM
    '''
    pass

def p_boolean(p):
    '''boolean : TRUE
               | FALSE
    '''
    pass

            # EOF
            # if (lexer.lexer.token() == None):
                # message = ' '.join(predict_set_dict[p.type])
                # raise StorytimeParsingError('Syntax Error: Expected {}'.format(message))

            # # Single Input
            # if (second_last_token == None):
                # raise StorytimeParsingError('Syntax Error: [{} {} {} {}]'.format(p.type, p.value, p.lineno, p.lexpos))

def p_error(p):
    if p:
        try:
            message = ' '.join(predict_set_dict[second_last_token.type])
            raise StorytimeParsingError('Syntax Error: Unexpected {} Expected {}'.format(p.value, message))
        except KeyError as error:
            raise StorytimeParsingError('Syntax Error: [{} {} {} {}]'.format(p.type, p.value, p.lineno, p.lexpos))
        except AttributeError as error:
            raise StorytimeParsingError('Syntax Error: [{} {} {} {}]'.format(p.type, p.value, p.lineno, p.lexpos))

def get_token():
    global last_token
    global second_last_token
    second_last_token = last_token
    last_token = lexer.lexer.token()
    return last_token

parser = yacc.yacc()

# while True:
    # try:
        # s = input('> ')
    # except EOFError:
        # break
    # if not s: continue
    # result = parser.parse(s, tokenfunc=get_token, debug=0)
