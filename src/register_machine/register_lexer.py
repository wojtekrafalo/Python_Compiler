import ply.lex as lex
from src.register_machine.register_token_list import tokens as tokens

tokens = tokens


def t_HALT(t):
    r'HALT'
    t.type = "HALT"
    return t


def t_COM_1(t):
    r'GET|PUT|LOAD|STORE|HALF|INC|DEC'
    t.type = "COM_1"
    return t


def t_COM_2(t):
    r'COPY|ADD|SUB'
    t.type = "COM_2"
    return t


def t_JUMP_1(t):
    r'JUMP'
    t.type = "JUMP_1"
    return t


def t_JUMP_2(t):
    r'JZERO|JODD'
    t.type = "JUMP_2"
    return t


def t_REG(t):
    r'[ABCDEFGH]'
    if t.value == "A":
        t.value = 0
    elif t.value == "B":
        t.value = 1
    elif t.value == "C":
        t.value = 2
    elif t.value == "D":
        t.value = 3
    elif t.value == "E":
        t.value = 4
    elif t.value == "F":
        t.value = 5
    elif t.value == "G":
        t.value = 6
    elif t.value == "H":
        t.value = 7
    t.type = "REG"
    return t


def t_LABEL(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = "LABEL"
    return t


def t_COMMENT(t):
    r'\#.*\n|\#.*$'
    t.type = "COMMENT"
    return t


t_NEW_LINE = r'\n'
t_SPACE = r'[ \t]+'


def t_error(t):
    r'.'
    # print("Syntax error")
    t.lexer.skip(1)
    print("Unexpected value:" + str(t.value))
    exit(-1)


lexer = lex.lex()
