import ply.lex as lex
from src.compiler.compiler_token_list import tokens as tokens
from src.compiler.compiler_token_list import TokensEnum
tokens = tokens

t_ignore = r' \n'
t_ignore_COMMENT = r'(\[[^\]]*\])'


class MyToken:
    def __init__(self, value, my_type):
        self.value = value
        self.token_type = my_type


def t_NUMBER(t):
    r'[0-9]+'
    num = int(t.value)
    t.value = MyToken(num, TokensEnum.NUMBER)
    return t


def t_IDENTIFIER(t):
    r'[_a-z]+'
    t.value = MyToken(t.value, TokensEnum.IDENTIFIER)
    return t


t_DECLARE = r'DECLARE'
t_IN = r'IN'
t_END = r'END'
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'
t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'
t_ENDDO = r'ENDDO'
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_ENDFOR = r'ENDFOR'
t_DOWNTO = r'DOWNTO'
t_READ = r'READ'
t_WRITE = r'WRITE'

t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_BRACKET_LEFT = r'\('
t_BRACKET_RIGHT = r'\)'
t_EQUALS = r'\='
t_NOT = r'\!'
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    r'.'
    # print("Syntax error")
    t.lexer.skip(1)
    print("Unexpected value: " + str(t.value))
    exit(-1)
    # return 'ERROR'


lexer = lex.lex()
